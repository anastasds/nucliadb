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

from datetime import datetime

try:
    from pydantic.v1 import BaseModel
except ImportError:
    from pydantic import BaseModel


class EnabledMetadata(BaseModel):
    text: bool
    entities: bool
    labels: bool
    vector: bool


class RequestData(BaseModel):
    created: datetime
    sentences: bool
    paragraphs: bool
    resources: bool
    fields: bool
    entities: bool
    labels: bool
    metadata: EnabledMetadata
