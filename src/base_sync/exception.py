import json

import requests

from .base_module import ModuleException


class ResponseException(ModuleException):
    """."""

    @classmethod
    def from_response(
            cls,
            response: requests.Response,
            msg: str = None,
            **kwargs
    ):
        try:
            exc_data: dict = response.json()
            raise cls(
                msg or exc_data.get('error'),
                data={
                    'error': exc_data.get('error'),
                    'params': exc_data.get('data', {}),
                    'kwargs': kwargs
                },
                code=response.status_code
            )
        except (ValueError, json.decoder.JSONDecodeError):
            text = response.text
            raise cls(
                msg or text,
                data={'error': text, 'kwargs': kwargs},
                code=response.status_code
            )

    @classmethod
    def unauthorized(cls):
        return cls('Требуется авторизация', code=401)

    @classmethod
    def forbidden(cls):
        return cls('Запрещено правами', code=403)


class FilerException(ResponseException):
    """."""
