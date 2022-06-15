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

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hellostreamingworld.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="hellostreamingworld.proto",
    package="hellostreamingworld",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x19hellostreamingworld.proto\x12\x13hellostreamingworld"3\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rnum_greetings\x18\x02 \x01(\t"\x1d\n\nHelloReply\x12\x0f\n\x07message\x18\x01 \x01(\t2b\n\x0cMultiGreeter\x12R\n\x08sayHello\x12!.hellostreamingworld.HelloRequest\x1a\x1f.hellostreamingworld.HelloReply"\x00\x30\x01\x62\x06proto3',
)


_HELLOREQUEST = _descriptor.Descriptor(
    name="HelloRequest",
    full_name="hellostreamingworld.HelloRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="hellostreamingworld.HelloRequest.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="num_greetings",
            full_name="hellostreamingworld.HelloRequest.num_greetings",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=50,
    serialized_end=101,
)


_HELLOREPLY = _descriptor.Descriptor(
    name="HelloReply",
    full_name="hellostreamingworld.HelloReply",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="message",
            full_name="hellostreamingworld.HelloReply.message",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=103,
    serialized_end=132,
)

DESCRIPTOR.message_types_by_name["HelloRequest"] = _HELLOREQUEST
DESCRIPTOR.message_types_by_name["HelloReply"] = _HELLOREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HelloRequest = _reflection.GeneratedProtocolMessageType(
    "HelloRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _HELLOREQUEST,
        "__module__": "hellostreamingworld_pb2"
        # @@protoc_insertion_point(class_scope:hellostreamingworld.HelloRequest)
    },
)
_sym_db.RegisterMessage(HelloRequest)

HelloReply = _reflection.GeneratedProtocolMessageType(
    "HelloReply",
    (_message.Message,),
    {
        "DESCRIPTOR": _HELLOREPLY,
        "__module__": "hellostreamingworld_pb2"
        # @@protoc_insertion_point(class_scope:hellostreamingworld.HelloReply)
    },
)
_sym_db.RegisterMessage(HelloReply)


_MULTIGREETER = _descriptor.ServiceDescriptor(
    name="MultiGreeter",
    full_name="hellostreamingworld.MultiGreeter",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=134,
    serialized_end=232,
    methods=[
        _descriptor.MethodDescriptor(
            name="sayHello",
            full_name="hellostreamingworld.MultiGreeter.sayHello",
            index=0,
            containing_service=None,
            input_type=_HELLOREQUEST,
            output_type=_HELLOREPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_MULTIGREETER)

DESCRIPTOR.services_by_name["MultiGreeter"] = _MULTIGREETER

# @@protoc_insertion_point(module_scope)