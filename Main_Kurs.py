import VK
import YD


if __name__ == '__main__':
    token_VK = '!!!!ТОКЕН VK!!!'
    screen_VK = 'antuanuran'

    token_YaDisk = '!! ТОКЕН YaDisk!!'
    name_folder_YaDisk = '_Folder_disk'

    vk_instance = VK.Vk_id(token_VK)
    dict_VK_result = vk_instance.name_result(screen_VK)

    yadisk_instance = YD.Load_yadisk(token_YaDisk)
    yadisk_instance.create_folder(name_folder_YaDisk)


    for i in dict_VK_result:
        name = f'{name_folder_YaDisk}/{dict_VK_result[i][0]}'
        url = dict_VK_result[i][2]
        yadisk_instance.upload_file_post(name, url)
        print(name)
        print('загружен...\n')

    yadisk_instance.upload_file_info(f'{name_folder_YaDisk}/files_info.txt', 'files_info.txt')




