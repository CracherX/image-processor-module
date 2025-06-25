from services.processor.base import BaseProcessor
from osgeo import gdal

class Scaler(BaseProcessor):
    def process(self, params):
        raise NotImplementedError()