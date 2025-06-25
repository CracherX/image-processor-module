import requests

from base_sync.base_module import ClassesLoggerAdapter

class _FilerBaseAPI:
    def __init__(
            self,
            url: str,
            con_timeout: int = 3,
            read_timeout: int = 30,
    ):
        self._logger = ClassesLoggerAdapter.create(self)
        self._url = url
        self._con_timeout = con_timeout
        self._read_timeout = read_timeout

class FilerExchangeService(_FilerBaseAPI):
    def upload_file(self, file_path: str, save_path_on_server: str, comment: str):
        url = f"{self._url}/files/file/"
        with open(file_path, 'rb') as f:
            files = {'upload': (file_path, f)}
            data = {
                'comment': comment,
                'path': save_path_on_server
            }
            response = requests.post(url, files=files, data=data,
                                     timeout=(self._con_timeout, self._read_timeout))
            print("ОТЛАДКА:", response.json())
            # TODO: убери потом

    def download_file(self, file_id, save_to: str):
        url = f"{self._url}/files/file/{file_id}/download/"
        response = requests.get(url, timeout=(self._con_timeout, self._read_timeout))

        if response.status_code == 200:
            with open(save_to, 'wb') as f:
                f.write(response.content)
        else:
            print("ОТЛАДКА Ошибка загрузки:", response.status_code, response.text)
            # TODO: убери потом
