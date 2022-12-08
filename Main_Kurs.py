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


    screen_VK = input("Введите Никнейм пользователя либо id (VK):  ")


    vk_instance = VK.Vk_id(token_VK)
    dict_VK_result = vk_instance.date_like_name_all(screen_VK)

    yadisk_instance = YD.Load_yadisk(token_YaDisk)
    yadisk_instance.create_folder(name_folder_YaDisk)


    for i in dict_VK_result:
        name = f'{name_folder_YaDisk}/{dict_VK_result[i][0]}'
        url = dict_VK_result[i][2]
        yadisk_instance.upload_file_post(name, url)
        print(name)
        print('загружен...\n')

    name_result(dict_VK_result)
    yadisk_instance.upload_file_info(f'{name_folder_YaDisk}/files_info.txt', 'files_info.txt')















