from osgeo import gdal

from models import Params
from services.processor.base import BaseProcessor


class Projector(BaseProcessor):
    def process(self, src_file: str, params: Params) -> str:
        result = src_file + '_processed.jp2'
        if params.target_projection:
            gdal.Warp(result, src_file, options=gdal.WarpOptions(
                dstSRS=params.target_projection,
            ))
        return result
