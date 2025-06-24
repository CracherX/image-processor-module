from config import config
from models import *  # noqa
from base_sync.injectors import PgConnectionInj

pg = PgConnectionInj(
    conf=config.pg,
)
