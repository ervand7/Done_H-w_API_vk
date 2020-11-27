import requests
from urllib.parse import urlencode, urljoin
from pprint import pprint

# # ____________________ 1-st stage: we get token ____________________________________________________
# #
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
    'Введите через пробел два id, которые вы хотите проанализировать на \nполучение общих друзей. '
    'Затем нажмите Enter: ').split(' ')
input_of_ids_items = list(map(int, input_of_ids))  # use for example: 280572200 435521107


# __________________________________________________________________________________________
# My main logic
class VKUser:
    def __init__(self, user_id=0, token=TOKEN, version=V, begin_url='https://vk.com/'):
        self.token = token
        self.version = version
        self.id = user_id
        self.begin_url = begin_url

    def __str__(self):
        url_of_user = urljoin(self.begin_url, f"id{str(self.id)}")
        return print(url_of_user)

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

        set_ = set()
        for i in response.json()['response']['items']:
            set_.add(i['id'])
        return set_

    def __and__(self, other):
        common_user_list = self.get_full_list_friends() & other.get_full_list_friends()
        return pprint(common_user_list)


# ```````````````````````````````````````````````````````````````````````````````````````
if __name__ == '__main__':
    man_1 = VKUser(input_of_ids_items[0])
    man_2 = VKUser(input_of_ids_items[1])
    man_1.__and__(man_2)
    man_1.__str__()
    man_2.__str__()
# use for example: 280572200 435521107
