import dataclasses as dc

from base_sync.base_module import Model


@dc.dataclass
class FilerErrorResponse(Model):
    data: dict = dc.field(default_factory=dict)
    error: str = dc.field(default=None)

@dc.dataclass
class FilerUploadRequest(Model):
    upload: bytes = dc.field()
    comment: str = dc.field(default="Выходной файл обработки")
    path: str = dc.field(default=None)
