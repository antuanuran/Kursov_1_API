import requests
import datetime


class VkPhoto:

    def __init__(self, token):
        self.token_str = token
        self.url_get_id = 'https://api.vk.com/method/users.get'
        self.url_get_photos = 'https://api.vk.com/method/photos.get'
        self.url_get = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def screen_id(self, screen_result):
        params = {
            'access_token': self.token_str,
            'user_ids': screen_result,
            'v': '5.131'
        }

        if not screen_result.isnumeric():
            resp_id = requests.get(self.url_get_id, params=params).json()

            # Проверка запроса-ответа
            response = requests.get(self.url_get_id, params=params).status_code
            if response == 200:
                print("\nзапрос 1 выполнен (никнейм переведен в id)...")
            else:
                exit(f"На этапе проверки перевода никнейма в id произошла ошибка, код ошибки: {response}! Перезапустите программу")

            # *****Проверка на корректность***********************************************
            try:
                return resp_id['response'][0]['id']

            except IndexError:
                exit("Введен некорректный никнейм, повторите попытку!")

        else:
            return screen_result

    def photo_id(self, screen_result):
        id_numb = self.screen_id(screen_result)
        print(f'(id) - {id_numb}')
        params = {
            'access_token': self.token_str,
            'owner_id': id_numb,
            'album_id': 'profile',
            'extended': 1,
            'v': '5.131'
        }

        photo = requests.get(self.url_get_photos, params=params).json()

        response = requests.get(self.url_get_photos, params=params).status_code
        if response == 200:
            print("\nзапрос 2 выполнен (получены данные из VK)...")
        else:
            exit(f"На этапе получения данных из VK произошла ошибка, код ошибки {response}! Перезапустите программу")

        # *****Проверка на корректность***********************************************
        try:
            photo_list_all = photo['response']['items']
            return photo_list_all

        except KeyError:
            exit("Ошибка данных! Запустите программу заново, введите корректные значения")

    def size_photo(self, screen_result):
        dict_photo = {}
        list_var = []
        for var in self.photo_id(screen_result):
            var_date = var['date']
            var_likes = var['likes']['count']
            var_2 = var['sizes']
            for i in var_2:
                list_var.append(i['width'])
            max_width = max(list_var)

            for i in var_2:
                if i['width'] == max_width:
                    link = i['url']
                    type_size = i['type']
            dict_photo[var_date] = [var_likes]
            dict_photo[var_date] += [link]
            dict_photo[var_date] += [type_size]

            list_var.clear()

        return dict_photo

    def date_like_name_all(self, screen_result):
        dict_all = self.size_photo(screen_result)
        list_all = []
        list_likes_unikal = []

        dict_name = {}

        for x in dict_all:
            x_date = x
            x_like = dict_all[x_date][0]
            x_link = dict_all[x_date][1]
            x_size = dict_all[x_date][2]

            date_name = datetime.datetime.fromtimestamp(x_date)
            x_date_result = date_name.strftime("%Y_%m_%d__%Hh.%Mm.%Ss")

            if x_like not in list_likes_unikal:
                list_likes_unikal.append(x_like)
                dict_name[x_date_result] = [f'{x_like}.jpg', x_size, x_link]

            else:
                dict_name[x_date_result] = [f'{x_like}._{x_date_result}.jpg', x_size, x_link]

        return dict_name
