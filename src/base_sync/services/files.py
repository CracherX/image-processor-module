import os
from email.parser import HeaderParser

import requests

from base_sync.base_module import ClassesLoggerAdapter
from base_sync.base_module import ModuleException


class _FilesBaseAPI:
    def __init__(
            self,
            url: str,
            auto_comment: str,
            server_save_path: str,
            con_timeout: int = 3,
            read_timeout: int = 30,
    ):
        self._logger = ClassesLoggerAdapter.create(self)
        self._url = url
        self._con_timeout = con_timeout
        self._read_timeout = read_timeout
        self._auto_comment = auto_comment
        self._server_save_path = server_save_path


class FilesStorageService(_FilesBaseAPI):
    def upload_file(self, file_path: str):
        url = f"{self._url}/api/files/file/"
        with open(file_path, 'rb') as f:
            files = {'upload': f}
            data = {
                'comment': self._auto_comment,
                'path': self._server_save_path,
            }
            response = requests.post(url, files=files, data=data,
                                     timeout=(self._con_timeout, self._read_timeout))
            if response.status_code != 200:
                raise ModuleException(
                    'Не удалось выгрузить результат обработки',
                    data=response.__dict__,
                    code=response.status_code
                )

    def download_file(self, file_id, save_to: str) -> str:
        url = f"{self._url}/api/files/file/{file_id}/download/"
        response = requests.get(url, timeout=(self._con_timeout, self._read_timeout))
        if response.status_code != 200:
            raise ModuleException(
                'Ошибка получения ответа файлового сервиса',
                data=response.__dict__,
                code=response.status_code
            )
        cd = response.headers.get('Content-Disposition')
        filename = self._parse_filename(cd)
        full_path = os.path.join(save_to, filename)
        if response.status_code == 200:
            with open(full_path, 'wb') as f:
                f.write(response.content)
            return full_path
        else:
            raise ModuleException('Тест', code=500)  # TODO: сделать модуль исключений клиента

    @staticmethod
    def _parse_filename(header_val: str) -> str:
        parser = HeaderParser()
        msg = parser.parsestr(f'Content-Disposition: {header_val}')
        return msg.get_filename()
