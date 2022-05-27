from pprint import pprint
import os
import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_file_list(self, file_path):
        file_list = []
        for file in os.listdir(file_path):
            if os.path.isfile(file):
                file_list.append(file)
        return file_list

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload(self, file_path: str):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str, ya_path: str):
        file_list = self.get_file_list(file_path)
        for file in file_list:
            href = self._get_upload(file_path=(ya_path + file)).get('href', "")
            response = requests.put(href, data=open(file, 'rb'))
            response.raise_for_status()
            if response.status_code == 201:
                print('Success')



if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_files = 'C:/Users/mikhasi/PycharmProjects/ya_task_request'
    path_to_yandexdisk = 'netology/'
    token = ''

    uploader = YaUploader(token)
    uploader.upload(path_to_files, path_to_yandexdisk)
