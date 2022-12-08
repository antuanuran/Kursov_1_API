import requests
class Load_yadisk:
    def __init__(self, token_YD):
        self.token_YD = token_YD
        self.headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'{self.token_YD}'
                       }
        self.url_get_file = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.url_get_folder = 'https://cloud-api.yandex.net/v1/disk/resources'


    def create_folder(self, name_folder):
        params = {
                    'path': name_folder
                 }
        requests.put(self.url_get_folder, headers=self.headers, params=params)

        response = requests.put(self.url_get_folder, headers=self.headers, params=params).status_code
        if response == 409:
            print("\nзапрос 3 выполнен (папка на Яндекс диске создана)...")



    def upload_file_post(self, name_disk, link):
       params = {
                    'path': name_disk,
                    'url': link
                }
       requests.post(self.url_get_file, headers=self.headers, params=params)

       response = requests.post(self.url_get_file, headers=self.headers, params=params).status_code
       if response == 202:
           print("\nзапрос выполнен (файл загружен)...")


    #Методы создания временной ссылки для загрузки файла
    def get_link(self, file_name):
        params = {
                    'path': file_name,
                    'overwrite': 'true'
                 }
        response = requests.get(self.url_get_file, headers=self.headers, params=params).json()
        return response['href']


    # Метод загрузки файла на яндекс диск
    def upload_file_info(self, disk_n, file_n):
        href = self.get_link(disk_n)
        requests.put(href, data=open(file_n, 'rb'))







