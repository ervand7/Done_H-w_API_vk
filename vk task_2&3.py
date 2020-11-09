import requests
from urllib.parse import urlencode, urljoin
from pprint import pprint
import tqdm

# ____________________ 1-st stage: we get token ____________________________________________________
#
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

# ____________________  2-nd stage: we already have the token  ____________________________________________________
TOKEN = 'c000969e3c270b9947bd26aea03beb35d31797026865f9f46da7459e45fb815b6d3a0e1644019c45ac6c9'
API_BASE_URL = 'https://api.vk.com/method/'
V = '5.21'

input_of_ids = input(
    'Введите через пробел два id, которые вы хотите проанализировать на \nполучение общих друзей. '
    'Затем нажмите Enter: ').split(' ')
input_of_ids_items = list(map(int, input_of_ids))  # use for example: 280572200 435521107


# __________________________________________________________________________________________
# My main logic
class VKUser:
    def __init__(self, user_id=0, token=TOKEN, version=V):
        self.token = token
        self.version = version
        self.id = user_id

    def count_of_all_friends(self):
        sheet_on_demand_vk = urljoin(API_BASE_URL, 'friends.search')
        response = requests.get(sheet_on_demand_vk, params={
            'access_token': self.token,
            'v': self.version,
            'user_id': self.id
        })
        s = int(response.json()['response']['count'])
        return s

    def get_full_list_friends(self):
        data_demand_of_vk = urljoin(API_BASE_URL, 'friends.search')
        response = requests.get(data_demand_of_vk, params={
            'access_token': self.token,
            'v': self.version,
            'user_id': self.id,
            'count': self.count_of_all_friends()
        })
        # check accurate count of friends
        # counter = 0
        # for i in response.json()['response']['items']:
        #     counter +=1
        # print(counter)

        set_ = set()
        for i in response.json()['response']['items']:
            set_.add(i['id'])
        return set_


man_1 = VKUser(input_of_ids_items[0])
man_2 = VKUser(input_of_ids_items[1])


def crossing(main_user=man_1, other_user=man_2):
    mutal_user_list = (main_user.get_full_list_friends()) & (other_user.get_full_list_friends())
    for i in tqdm.tqdm(sorted(mutal_user_list)):
        pprint(i)


crossing()

print(f'\nВыше был представлен список бщих друзей между пользователями \n'
      f'с id {input_of_ids_items[0]} и {input_of_ids_items[1]}.')
# __________________________________________________________________________________________
# url getting

print('\nА это ссылки на их профили:')
begin_url = 'https://vk.com/'
man_1_url = urljoin(begin_url, f"id{str(input_of_ids_items[0])}")
man_2_url = urljoin(begin_url, f"id{str(input_of_ids_items[1])}")
print(man_1_url)
print(man_2_url)