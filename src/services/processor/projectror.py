import dataclasses as dc

from osgeo import gdal

from base_sync.base_module import Model
from services.processor.base import BaseProcessor


@dc.dataclass
class Params(Model):
    target_projection: str = dc.field()


class Projector(BaseProcessor):
    ALGORITHM = 'PROJECTION'

    def process(self, src_file: str, params: dict) -> str:
        result = src_file + '_processed.jp2'
        params = Params.load(params)
        gdal.Warp(result, src_file, options=gdal.WarpOptions(
            dstSRS=params.target_projection,
        ))
        return result
