import VK
import YD
import configparser
import json


def name_result(result_info_json):
    dict_all = result_info_json
    list_info = []

    for i in dict_all:
        a = {}
        a['file_name'] = dict_all[i][0]
        a['size'] = dict_all[i][1]
        list_info.append(a)

    with open('info_files.json', 'w') as a:
        json.dump(list_info, a)





if __name__ == '__main__':

    # Загрузка с config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    token_VK = config['Token']['token_VK']
    token_YaDisk = config['Token']['token_YaDisk']
    name_folder_YaDisk = config['Folder']['name_folder_YaDisk']

    # Ввод данных
    replay = 1
    while replay == 1:
        try:
            screen_VK = input("Введите Никнейм пользователя либо id (VK):  ")
            count_photo = int(input("Введите кол-во фотографий для скачивания:  "))
            replay = 2

        except ValueError:
            print("Введены некорректные данные, повторите попытку!\n")

    # Запуск Метода VK
    vk_instance = VK.VkPhoto(token_VK)
    dict_VK_result = vk_instance.date_like_name_all(screen_VK)

    # Запуск Метода YaDisk
    yadisk_instance = YD.LoadYadisk(token_YaDisk)
    yadisk_instance.create_folder(name_folder_YaDisk)

    # Загрузка на yaDisk + проверка на кол-во фото
    count = 0
    for i in dict_VK_result:
        name = f'{name_folder_YaDisk}/{dict_VK_result[i][0]}'
        url = dict_VK_result[i][2]

        if count < count_photo:
            yadisk_instance.upload_file_post(name, url)
            print(name)
            count += 1

    if count_photo == count:
        print("\nВсе фото успешно загружены!")
    else:
        print("\nПрограмма успешно загрузила все фото профиля. Вами было введено количество, превышающее фото в профиле.")

    # Запуск Метода информационного файла загрузки данных
    name_result(dict_VK_result)
    yadisk_instance.upload_file_info(f'{name_folder_YaDisk}/info_files.json', 'info_files.json')


