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
from collections.abc import AsyncGenerator
from typing import Callable
from unittest import mock

import pytest
from httpx import AsyncClient

from nucliadb.reader.api.v1.router import KB_PREFIX
from nucliadb_models.notifications import (
    Notification,
    ResourceIndexedNotification,
    ResourceProcessedNotification,
    ResourceWrittenNotification,
)
from nucliadb_models.resource import NucliaDBRoles
from nucliadb_protos import writer_pb2


@pytest.fixture(scope="function")
def kb_notifications():
    async def _kb_notifications(
        kbid: str,
    ) -> AsyncGenerator[writer_pb2.Notification, None]:
        for notification in [
            writer_pb2.Notification(
                kbid=kbid,
                seqid=1,
                uuid="resource",
                write_type=writer_pb2.Notification.WriteType.CREATED,
                action=writer_pb2.Notification.Action.COMMIT,
                source=writer_pb2.NotificationSource.WRITER,
            ),
            writer_pb2.Notification(
                kbid=kbid,
                seqid=1,
                uuid="resource",
                write_type=writer_pb2.Notification.WriteType.CREATED,
                action=writer_pb2.Notification.Action.COMMIT,
                source=writer_pb2.NotificationSource.PROCESSOR,
                processing_errors=True,
            ),
            writer_pb2.Notification(
                kbid=kbid,
                seqid=1,
                uuid="resource",
                write_type=writer_pb2.Notification.WriteType.CREATED,
                action=writer_pb2.Notification.Action.INDEXED,
            ),
        ]:
            await asyncio.sleep(0.001)
            yield notification

    with mock.patch(
        "nucliadb.reader.reader.notifications.kb_notifications", new=_kb_notifications
    ) as mocked:
        yield mocked


@pytest.mark.asyncio
async def test_activity(
    kb_notifications,
    reader_api,
    knowledgebox_ingest,
):
    kbid = knowledgebox_ingest
    async with reader_api(roles=[NucliaDBRoles.READER]) as client:
        async with client.stream(
            method="GET",
            url=f"/{KB_PREFIX}/{kbid}/notifications",
        ) as resp:
            assert resp.status_code == 200

            notifs = []
            async for line in resp.aiter_lines():
                notification_type = Notification.parse_raw(line).type
                assert notification_type in [
                    "resource_indexed",
                    "resource_written",
                    "resource_processed",
                ]

                if notification_type == "resource_indexed":
                    notif = ResourceIndexedNotification.parse_raw(line)
                    assert notif.type == "resource_indexed"
                    assert notif.data.resource_uuid == "resource"
                    assert notif.data.seqid == 1

                elif notification_type == "resource_written":
                    notif = ResourceWrittenNotification.parse_raw(line)
                    assert notif.type == "resource_written"
                    assert notif.data.resource_uuid == "resource"
                    assert notif.data.seqid == 1
                    assert notif.data.operation == "created"
                    assert notif.data.error is False

                elif notification_type == "resource_processed":
                    notif = ResourceProcessedNotification.parse_raw(line)
                    assert notif.type == "resource_processed"
                    assert notif.data.resource_uuid == "resource"
                    assert notif.data.seqid == 1
                    assert notif.data.ingestion_succeeded is True
                    assert notif.data.processing_errors is True

                else:
                    assert False, "Unexpected notification type"

                notifs.append(notif)

        assert len(notifs) == 3


@pytest.mark.asyncio
async def test_activity_kb_not_found(
    reader_api: Callable[..., AsyncClient],
):
    async with reader_api(roles=[NucliaDBRoles.READER]) as client:
        resp = await client.get(f"/{KB_PREFIX}/foobar/notifications")
        assert resp.status_code == 404
