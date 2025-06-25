from services.processor.base import BaseProcessor
from osgeo import gdal

class Projector(BaseProcessor):
    def process(self, params):
        raise NotImplementedError()