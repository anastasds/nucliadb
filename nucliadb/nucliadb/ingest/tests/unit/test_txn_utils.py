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
from unittest.mock import AsyncMock, patch

import pytest

from nucliadb.ingest import txn_utils

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def driver():
    mock = AsyncMock()
    with patch("nucliadb.ingest.txn_utils.get_driver", return_value=mock):
        yield mock


async def test_get_transaction_auto_aborts(driver) -> None:
    async def mytask():
        await txn_utils.get_transaction()

    await asyncio.create_task(mytask())

    await asyncio.sleep(0.05)

    driver.begin.return_value.abort.assert_called_once()
