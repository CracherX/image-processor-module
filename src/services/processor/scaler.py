from base_sync.base_module import ModuleException
from models import Params
from services.processor.base import BaseProcessor
from osgeo import gdal

class Scaler(BaseProcessor):
    def process(self, src_file: str, params: Params) -> str:
        result = src_file + '_processed.jp2'
        args = {
        }
        if params.scale_x is None and params.scale_y is None:
            raise ModuleException('Не указаны параметры обработки для изменения разрешения')
        if params.scale_x: args['xRes'] = params.scale_x
        if params.scale_y: args['yRes'] = params.scale_y
        gdal.Warp(result, src_file, options=gdal.WarpOptions(
            **args
        ))
        return result
