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
TOKEN = ''
API_BASE_URL = 'https://api.vk.com/method/'
V = '5.21'

input_of_ids = input(
    'Введите через пробел два id, которые вы хотите проанализировать на получение общих друзей. '
    'Затем нажмите Enter: ').split(' ')
two_ids = list(map(int, input_of_ids))  # use for example: 280572200 435521107


class VKUser_1:
    def __init__(self, token=TOKEN, version=V, id=two_ids[0]):
        self.token = token
        self.version = version
        self.id = id

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
        status_common_lst = urljoin(API_BASE_URL, 'friends.search')
        response = requests.get(status_common_lst, params={
            'access_token': self.token,
            'v': self.version,
            'user_id': self.id,
            'count': a.count_of_all_friends()
        })
        # check accurate count of friends
        # counter = 0
        # for i in response.json()['response']['items']:
        #     counter +=1
        # print(counter)

        set_1 = set()
        for i in response.json()['response']['items']:
            set_1.add(i['id'])
        return set_1


a = VKUser_1()


class VKUser_2:
    def __init__(self, token=TOKEN, version=V, id=two_ids[1]):
        self.token = token
        self.version = version
        self.id = id

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
        status_common_lst = urljoin(API_BASE_URL, 'friends.search')
        response = requests.get(status_common_lst, params={
            'access_token': self.token,
            'v': self.version,
            'user_id': self.id,
            'count': b.count_of_all_friends()
        })
        # check accurate count of friends
        # counter = 0
        # for i in response.json()['response']['items']:
        #     counter +=1
        # print(counter)

        set_2 = set()
        for i in response.json()['response']['items']:
            set_2.add(i['id'])
        return set_2


b = VKUser_2()


def finder_common_friends(first_user, second_user):
    common_friends_id = list(first_user.get_full_list_friends() & second_user.get_full_list_friends())
    for i in tqdm.tqdm(sorted(common_friends_id)):
        pprint(i)
    print(f'Это был список с id общих друзей в ВК между аккаунтами с id {two_ids[0]} и {two_ids[1]}.')


finder_common_friends(a, b)

begin_url = 'https://vk.com/'
user_1_url = urljoin(begin_url, f"id{str(two_ids[0])}")
user_2_url = urljoin(begin_url, f"id{str(two_ids[1])}")
print(user_1_url)
print(user_2_url)