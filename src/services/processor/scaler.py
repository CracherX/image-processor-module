import dataclasses as dc

from osgeo import gdal

from base_sync.base_module import Model
from services.processor.base import BaseProcessor


@dc.dataclass
class Params(Model):
    scale_x: int = dc.field()
    scale_y: int = dc.field()


class Scaler(BaseProcessor):
    ALGORITHM = 'SCALING'

    def process(self, src_file: str, params: dict) -> str:
        result = src_file + '_processed.jp2'
        params = Params.load(params)
        gdal.Warp(result, src_file, options=gdal.WarpOptions(
            xRes=params.scale_x,
            yRes=params.scale_y,
        ))
        return result
