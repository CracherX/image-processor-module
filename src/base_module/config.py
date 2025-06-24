import dataclasses as dc
import os

from .model import Model


@dc.dataclass
class PgConfig(Model):
    """."""

    host: str = dc.field()
    port: int = dc.field()
    user: str = dc.field()
    password: str = dc.field()
    database: str = dc.field()
    max_pool_connections: int = dc.field(default=100)
    debug: bool = dc.field(default=False)
    schema: str = dc.field(default='public')


@dc.dataclass
class ProcessorPgConfig(PgConfig):
    """."""

    host: str = dc.field(default=os.getenv('PG_HOST', "localhost"))
    port: int = dc.field(default=int(os.getenv('PG_PORT', 5432)))
    user: str = dc.field(default=os.getenv('PG_USER', 'Test'))
    password: str = dc.field(default=os.getenv('PG_PASSWORD', 'Test'))
    database: str = dc.field(default=os.getenv('PG_DATABASE', 'Processor'))

@dc.dataclass
class _CredentialsConfig(Model):
    """."""

    host: str = dc.field(default='rabbit')
    port: int = dc.field(default=5672)
    user: str = dc.field(default='admin')
    password: str = dc.field(default='12345')


@dc.dataclass
class RabbitPublisherConfig(_CredentialsConfig):
    """."""

    exchange: str = dc.field(default='')
    routing_key: str = dc.field(default='')
    reply_to: str = dc.field(default=None)


@dc.dataclass
class RabbitConsumerConfig(_CredentialsConfig):
    """."""

    queue_name: str = dc.field(default='')
    error_timeout: int = dc.field(default=10)
    max_priority: int = dc.field(default=5)


@dc.dataclass
class RabbitFullConfig(RabbitConsumerConfig, RabbitPublisherConfig):
    """."""
