# Copyright (C) 2021 Bosutech XXI S.L.
#
# nucliadb is offered under the AGPL v3.0 and as commercial software.
# For commercial licensing, contact us at info@nuclia.com.
#
# AGPL:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import asyncio
import contextlib
import uuid
from collections.abc import AsyncGenerator

import async_timeout

from nucliadb.reader import logger
from nucliadb_models.notifications import (
    Notification,
    ResourceIndexed,
    ResourceIndexedNotification,
    ResourceOperationType,
    ResourceProcessed,
    ResourceProcessedNotification,
    ResourceWritten,
    ResourceWrittenNotification,
)
from nucliadb_protos import writer_pb2
from nucliadb_telemetry.errors import capture_exception
from nucliadb_utils import const
from nucliadb_utils.cache.pubsub import Callback, PubSubDriver
from nucliadb_utils.utilities import get_pubsub

MAX_QUEUE_SIZE = 1000

# We set the timeout to slightly less than the
# configured K8S max connection timeout, which is 2 minutes
NOTIFICATIONS_TIMEOUT_S = 118

RESOURCE_OP_PB_TO_MODEL = {
    writer_pb2.Notification.WriteType.UNSET: ResourceOperationType.CREATED,
    writer_pb2.Notification.WriteType.CREATED: ResourceOperationType.CREATED,
    writer_pb2.Notification.WriteType.MODIFIED: ResourceOperationType.MODIFIED,
    writer_pb2.Notification.WriteType.DELETED: ResourceOperationType.DELETED,
}


async def kb_notifications_stream(kbid: str) -> AsyncGenerator[bytes, None]:
    """
    Returns an async generator that yields pubsub notifications for the given kbid.
    The generator will return after NOTIFICATIONS_TIMEOUT_S seconds.
    """
    try:
        async with async_timeout.timeout(NOTIFICATIONS_TIMEOUT_S):
            async for pb_notification in kb_notifications(kbid):
                line = encode_streamed_notification(pb_notification) + b"\n"
                yield line
    except asyncio.TimeoutError:
        return


async def kb_notifications(kbid: str) -> AsyncGenerator[writer_pb2.Notification, None]:
    """
    Returns an async generator that yields pubsub notifications for the given kbid.
    """
    pubsub = await get_pubsub()
    if pubsub is None:  # pragma: no cover
        logger.warning("PubSub is not configured")
        return

    queue: asyncio.Queue = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)

    subscription_key = const.PubSubChannels.RESOURCE_NOTIFY.format(kbid=kbid)

    def subscription_handler(raw_data: bytes):
        data = pubsub.parse(raw_data)
        notification = writer_pb2.Notification()
        notification.ParseFromString(data)
        # We don't need the whole broker message, so we clear it to
        # save space, as it can potentially be very big
        notification.ClearField("message")
        try:
            queue.put_nowait(notification)
        except asyncio.QueueFull:  # pragma: no cover
            logger.warning("Queue is full, dropping notification", extra={"kbid": kbid})

    async with managed_subscription(
        pubsub, key=subscription_key, handler=subscription_handler
    ):
        try:
            while True:
                notification: writer_pb2.Notification = await queue.get()
                yield notification
        except Exception as ex:
            capture_exception(ex)
            logger.error(
                "Error while streaming activity", exc_info=True, extra={"kbid": kbid}
            )
            return


@contextlib.asynccontextmanager
async def managed_subscription(pubsub: PubSubDriver, key: str, handler: Callback):
    # We assign a random group to the subscription so that each reader gets all notifications.
    subscription_id = group = uuid.uuid4().hex

    await pubsub.subscribe(
        handler=handler,
        key=key,
        group=group,
        subscription_id=subscription_id,
    )
    try:
        yield
    finally:
        try:
            await pubsub.unsubscribe(key=key, subscription_id=subscription_id)
        except Exception:  # pragma: no cover
            logger.warning(
                "Error while unsubscribing from activity stream", exc_info=True
            )


def serialize_notification(pb: writer_pb2.Notification) -> Notification:
    resource_uuid = pb.uuid
    seqid = pb.seqid

    if pb.action == writer_pb2.Notification.Action.INDEXED:
        return ResourceIndexedNotification(
            data=ResourceIndexed(
                resource_uuid=resource_uuid,
                seqid=seqid,
            )
        )

    has_ingestion_error = pb.action == writer_pb2.Notification.Action.ABORT
    has_processing_error = pb.processing_errors

    if pb.source == writer_pb2.NotificationSource.WRITER:
        writer_operation = RESOURCE_OP_PB_TO_MODEL[pb.write_type]
        return ResourceWrittenNotification(
            data=ResourceWritten(
                resource_uuid=resource_uuid,
                seqid=seqid,
                operation=writer_operation,
                error=has_ingestion_error,
            )
        )
    elif pb.source == writer_pb2.NotificationSource.PROCESSOR:
        return ResourceProcessedNotification(
            data=ResourceProcessed(
                resource_uuid=resource_uuid,
                seqid=seqid,
                ingestion_succeeded=not has_ingestion_error,
                processing_errors=has_processing_error,
            )
        )

    raise ValueError(f"Unknown notification source: {pb.source}")


def encode_streamed_notification(pb: writer_pb2.Notification) -> bytes:
    notification = serialize_notification(pb)
    encoded_nofication = notification.json().encode("utf-8")
    return encoded_nofication
