import requests
from urllib.parse import urlencode, urljoin  # это поможет в получении токена ВК
from pprint import pprint
import json
import os  # для создание платформо-независимого путя к файлу
# следующие 2 модуля нужны чтобы получить расширение у url
from urllib.parse import urlparse
from os.path import splitext, basename

from itertools import islice  # быстро разбить словарь на несколько словарей
from tqdm import tqdm  # прогресс-бар

# ____________________ instruction for getting VK token  ____________________________________________________
# oauth_api_base_url = 'https://oauth.vk.com/authorize'
# APP_ID = 7649081
# redirect_uri = 'https://oauth.vk.com/blank.html'
# scope = 'friends'
#
# oauth_params = {
#     'redirect_uri': redirect_uri,
#     'scope': scope,
#     'response_type': 'token',
#     'client_id': APP_ID
# }
#
# print('?'.join([oauth_api_base_url, urlencode(oauth_params)]))


# __________________________________________________________________
# Блок токенов
VK_TOKEN = 'c14c6dd20e646cc5b7d39a0f64d5cca161025fc579b4b440e221f6ed2b78a5c00dd19609d3d6da2eba8ea'
API_BASE_URL = 'https://api.vk.com/method/'
V = '5.21'

YANDEX_TOKEN = 'AgAAAAA6wCXpAADLW3o9UKJyK0n6qX3OfUgGEWI'

# __________________________________________________________________
# Блок ввода данных
for_vk_input = input(
    'Введите через пробел id пользователя и кол-во фотографий, нужных вам. '
    'Затем нажмите Enter. \nВнимание! Cервис Яндекс.Диск может выдать меньшее кол-во фото, чем вы запрашиваете.\n'
    'Итак, введите через пробел id и кол-во фото : ').split(
    ' ')
for_vk_input_items = list(map(int, for_vk_input))  # use for example: 280572200 12

folder_input = str(input('\nВведите название папки, которая будет располагаться на Яндекс.Диске,\n'
                         'в которую затем будут загружены фотки из соцсетей: '))  # use for example: My_new_folder

json_input = str(
    input(
        '\nВведите название json-файла (без ковычек и расширения), он автоматически создастся,'
        '\nи в него будем записывать данные о фото: '))


# __________________________________________________________________
# Работаем с ВК и в итоге получаем переменную lst_of_small_dicts, в которой у нас будут все
# названия, требуемые в задании, ссылки, размеры и тд. Потом, уже на основе этой переменной
# будет создан json-файл и, опять же, на основе итерации по этой переменной, будет загрузка в Яндека.Диск
class VKUser:
    def __init__(self, token=VK_TOKEN, version=V, id=for_vk_input_items[0], count=for_vk_input_items[1]):
        self.token = token
        self.version = version
        self.count = count
        self.owner_id = id

    def get_list_of_fourth_task_paragraph(self):
        data_for_vk = urljoin(API_BASE_URL, 'photos.get')
        # print(data_for_vk)
        response = requests.get(data_for_vk, params={
            'access_token': self.token,
            'v': self.version,
            'owner_id': self.owner_id,
            'album_id': 'profile',
            'extended': 1,
            'count': self.count
        })

        # __________________________________________________________________
        # Получаем фотки в виде списка, каждое значение из которого: лайк - ссылка - дата
        lst_like_link_date = []
        res = response.json()['response']['items']
        # pprint(res)
        for i in res:
            if 'photo_2560' in i:
                a = (i['likes']['count'], i['photo_2560'], i['date'])
                lst_like_link_date.append(list(a))
            elif 'photo_1280' in i:
                a = (i['likes']['count'], i['photo_1280'], i['date'])
                lst_like_link_date.append(list(a))
            elif 'photo_807' in i:
                a = (i['likes']['count'], i['photo_807'], i['date'])
                lst_like_link_date.append(list(a))
            elif 'photo_604' in i:
                a = (i['likes']['count'], i['photo_604'], i['date'])
                lst_like_link_date.append(list(a))
            elif 'photo_130' in i:
                a = (i['likes']['count'], i['photo_130'], i['date'])
                lst_like_link_date.append(list(a))
            elif 'photo_75' in i:
                a = (i['likes']['count'], i['photo_75'], i['date'])
                lst_like_link_date.append(list(a))
        # print(counter_of_sizes)
        # print(lst_like_link_date)

        # __________________________________________________________________
        # Получаем расширение и прилепляем его к str_показателю кол-ва лайков
        for i in lst_like_link_date:  # Для этого используем from os.path import splitext, basename и from urllib.parse import urlparse
            picture_page = i[1]
            disassembled = urlparse(picture_page)
            filename, file_ext = splitext(basename(disassembled.path))  # теперь у нас отдельно есть file_ext
            i[0] = str(i[0]) + '_ext_' + file_ext
        # pprint(lst_like_link_date)

        # __________________________________________________________________
        # Если название, оно же и str_показатель кол-ва лайков, уже есть в update_lst_like_link_date,
        # то мы к его названию еще прилепляем и дату загузки (такое условие у задания).
        # Ну и, соответственно, в update_lst_like_link_date мы уже не берем последний элемент
        # из lst_like_link_date, то есть date, так как сейчас
        # мы с ним поработали, от него взяли все нужное, и больше он нам не нужен.
        update_lst_like_link_date = []
        for i in lst_like_link_date:
            if i[0] in [d[0] for d in update_lst_like_link_date]:
                i[0] = 'date_' + str(i[2]) + '|name_' + i[0]
            update_lst_like_link_date.append(i[0:2])
        # pprint(update_lst_like_link_date)

        # __________________________________________________________________
        # Теперь трансформируем update_lst_like_link_date в словарь single_dct_name_link,
        # в котором ключ - это название файла, а значение - ссылка.
        # Этот словарь нужен, чтобы потом его разбить на словарь словарей и далее уже
        # значения подгонять под нужные нам параметры.
        single_dct_name_link = {}
        for i in update_lst_like_link_date:
            single_dct_name_link[i[0]] = i[1]

        # pprint(single_dct_name_link)

        # __________________________________________________________________
        # Теперь разбиваем словарь на мелкие словари (имя: ссылка) и оборачиваем их в список
        def chunks(data, SIZE=0):  # используем from itertools import islice
            it = iter(data)
            for i in range(0, len(data), SIZE):
                yield {k: data[k] for k in islice(it, SIZE)}

        lst_of_small_dicts = []
        for item in chunks({i: a for i, a in single_dct_name_link.items()}, 1):
            lst_of_small_dicts.append(item)
        # pprint(lst_of_small_dicts) # получили словарь словарей

        # __________________________________________________________________
        # Лепим из этого lst_of_small_dicts, элементы которого
        # сейчас представляют собой название: ссылка, нужные нам параметры.
        # Тут мы как бы сдвигаем ключ в значение, а на месте ключа прописываем 'file_name'
        for i in lst_of_small_dicts:
            for name_with_ext in list(i):  # Оборачивая i в list мы избег. ош.: dictionary changed size during iteration
                i['file_name'] = name_with_ext

        # Берем наш изначальный элемент i (словарь, которых много в списке lst_of_small_dicts)
        # и создаем внутри этого словаря новый ключ 'file_link', и даем ему значение
        # изначального ключа, то есть ссылку.
        for i in lst_of_small_dicts:
            for key in list(i):  # Оборачивая i в list мы избег. ош.: dictionary changed size during iteration
                if '_ext_' in key:
                    i['file_link'] = i[key]

        # Все сделали. Избавляемся теперь от ненужного изначального элемента название - ссылка.
        for i in lst_of_small_dicts:
            for key in list(i):  # Оборачивая i в list мы избег. ош.: dictionary changed size during iteration
                if '_ext_' in key:
                    i.pop(key)  # удаляем ключ, а вместе с ним и значение
        return lst_of_small_dicts


experimental = VKUser()


# __________________________________________________________________
# Процесс создания папки на Яндекс.Диске
class YandexFolderCreating:
    def __init__(self, folder_name=folder_input, token=YANDEX_TOKEN):
        self.token = token
        self.folder_name = folder_name

        requests.put(
            "https://cloud-api.yandex.net/v1/disk/resources",
            params={"path": self.folder_name},
            headers={"Authorization": f"OAuth {YANDEX_TOKEN}"}
        )
        print(f'The folder with name "{folder_name}" is successfully created on Yandex.Disk.')


yandex_disk_folder = YandexFolderCreating()

# __________________________________________________________________
# Процесс создания json-файла и записи в него
json_file = dict()
json_file['info'] = experimental.get_list_of_fourth_task_paragraph()

file_path = os.path.join(os.getcwd(), f'{json_input}.json')
with open(file_path, 'w+') as f:
    json.dump(json_file, f, ensure_ascii=False, indent=2)

print(
    f'\nДанные в требуемом заданием формате успешно записаны в \n'
    f'только что созданный вами json-файл под названием "{json_input}.json".'
    f'\nЭтот json-файл вы можете найти в памяти своего ПК.')


# __________________________________________________________________
# Процесс записи данных в Яндекс.Диск из переменной lst_of_small_dicts, которая является
# результатом от experimental.get_list_of_fourth_task_paragraph()
class YaUpPhotoFromVk:
    def __init__(self, token=YANDEX_TOKEN):
        self.token = token
        for i in tqdm(experimental.get_list_of_fourth_task_paragraph()):
            requests.post(
                "https://cloud-api.yandex.net/v1/disk/resources/upload",
                params={"url": i["file_link"],
                        "path": f'{folder_input}/{i["file_name"]}'},
                headers={"Authorization": f"OAuth {YANDEX_TOKEN}", }
            )


print('\nПожалуйста, подождите. Идет загрузка файлов на Яндекс.Диск.')
yandex_uploader = YaUpPhotoFromVk()
print(
    f'Фотографии максимального размера ({for_vk_input_items[1]} шт.) '
    f'успешно загружены на Яндекс.Диск в папку под названием "{folder_input}".')
