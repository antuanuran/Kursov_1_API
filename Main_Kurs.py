import VK
import YD
import configparser


def name_result(result_info_json):
    with open('files_info.txt', 'w') as a:
        a.writelines(result_info_json)


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

    # Запуск Метода информационного файла загрузки данных
    name_result(dict_VK_result)
    yadisk_instance.upload_file_info(f'{name_folder_YaDisk}/files_info.txt', 'files_info.txt')
