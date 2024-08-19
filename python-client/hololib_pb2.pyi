from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HelloRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class HologramRequest(_message.Message):
    __slots__ = ("meshDataSize", "meshData", "textureDataSize", "textureData", "shadingOption", "textureOption", "wavelengthOption", "pixelSizeOption", "numOfPixelsOption", "initialPhaseOption")
    MESHDATASIZE_FIELD_NUMBER: _ClassVar[int]
    MESHDATA_FIELD_NUMBER: _ClassVar[int]
    TEXTUREDATASIZE_FIELD_NUMBER: _ClassVar[int]
    TEXTUREDATA_FIELD_NUMBER: _ClassVar[int]
    SHADINGOPTION_FIELD_NUMBER: _ClassVar[int]
    TEXTUREOPTION_FIELD_NUMBER: _ClassVar[int]
    WAVELENGTHOPTION_FIELD_NUMBER: _ClassVar[int]
    PIXELSIZEOPTION_FIELD_NUMBER: _ClassVar[int]
    NUMOFPIXELSOPTION_FIELD_NUMBER: _ClassVar[int]
    INITIALPHASEOPTION_FIELD_NUMBER: _ClassVar[int]
    meshDataSize: int
    meshData: bytes
    textureDataSize: int
    textureData: bytes
    shadingOption: str
    textureOption: str
    wavelengthOption: str
    pixelSizeOption: str
    numOfPixelsOption: str
    initialPhaseOption: str
    def __init__(self, meshDataSize: _Optional[int] = ..., meshData: _Optional[bytes] = ..., textureDataSize: _Optional[int] = ..., textureData: _Optional[bytes] = ..., shadingOption: _Optional[str] = ..., textureOption: _Optional[str] = ..., wavelengthOption: _Optional[str] = ..., pixelSizeOption: _Optional[str] = ..., numOfPixelsOption: _Optional[str] = ..., initialPhaseOption: _Optional[str] = ...) -> None: ...

class HologramReply(_message.Message):
    __slots__ = ("hologramDataSize", "hologramData", "ReconstDataSize", "ReconstData", "duration")
    HOLOGRAMDATASIZE_FIELD_NUMBER: _ClassVar[int]
    HOLOGRAMDATA_FIELD_NUMBER: _ClassVar[int]
    RECONSTDATASIZE_FIELD_NUMBER: _ClassVar[int]
    RECONSTDATA_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    hologramDataSize: int
    hologramData: bytes
    ReconstDataSize: int
    ReconstData: bytes
    duration: int
    def __init__(self, hologramDataSize: _Optional[int] = ..., hologramData: _Optional[bytes] = ..., ReconstDataSize: _Optional[int] = ..., ReconstData: _Optional[bytes] = ..., duration: _Optional[int] = ...) -> None: ...
