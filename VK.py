import requests
import datetime
from pprint import pprint

class Vk_id:

    def __init__(self, token):
        # https://dev.vk.com/method/users.get   |   https://dev.vk.com/method/photos.get
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

        if screen_result.isnumeric() == False:
            resp_id = requests.get(self.url_get_id, params=params).json()
            return resp_id['response'][0]['id']

        else:
            return screen_result


    def photo_id(self, screen_result):
        id = self.screen_id(screen_result)
        print(f'(id) - {id} | Никнейм: @{screen_result} \n')
        params = {
                    'access_token': self.token_str,
                    'owner_id': id,
                    'album_id': 'profile',
                    'extended': 1,
                    'v': '5.131'
        }

        photo = requests.get(self.url_get_photos, params=params).json()
        photo_list_all = photo['response']['items']
        # pprint(photo_list_all)
        return photo_list_all


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

        # pprint(dict_photo)
        return dict_photo


    def date_like_name_all(self, screen_result):
        dict_all = self.size_photo(screen_result)
        # pprint(dict_all)
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



    def name_result (self, screen_result):
        info_files = self.date_like_name_all(screen_result)
# *************
        result_dict = {}

        for temp in info_files:
            result_dict[info_files[temp][0]] = 'file_name'
            result_dict[info_files[temp][1]] = 'max size   |'

        with open('files_info.txt', 'w') as a:
            a.writelines(f'Информация по файлам, записанным на диск: \n {result_dict}')

# **********
        return info_files










