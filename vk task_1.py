import requests
from urllib.parse import urlencode, urljoin
from pprint import pprint
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

class VKUser:
    def __init__(self, token=TOKEN, version=V):
        self.token = token
        self.version = version

    def get_common_friends(self):
        status_common_lst = urljoin(API_BASE_URL, 'friends.getMutual')
        print(status_common_lst)
        response = requests.get(status_common_lst, params={
            'access_token': self.token,
            'v': self.version,
            'target_uid': 280572200,
            'source_uid': 435521107
        })
        n = sorted(response.json()['response'])
        for i in n:
            pprint(i)

a = VKUser()
a.get_common_friends()


