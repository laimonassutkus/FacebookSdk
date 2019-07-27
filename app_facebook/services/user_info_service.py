import requests

from typing import Tuple
from django.conf import settings


class UserInfoService:
    __instance = None
    __API_VERSION = 'v3.2'

    def __new__(cls):
        if UserInfoService.__instance is None:
            UserInfoService.__instance = object.__new__(cls)

            cls.__access_token = settings.FACEBOOK_ACCESS_TOKEN

        return UserInfoService.__instance

    def info(self, facebook_user_id: str) -> Tuple[str, str, str]:
        endpoint = self.__create_endpoint(facebook_user_id)

        resp = requests.get(url=endpoint)

        if resp.status_code != 200:
            raise ValueError('Could not get user {} info from FB API. Reason: {}'.format(facebook_user_id, resp.text))

        resp = resp.json()

        name = resp['first_name']
        surname = resp['last_name']
        profile_pic = resp['profile_pic']

        return name, surname, profile_pic

    def __create_endpoint(self, user: str) -> str:
        return "https://graph.facebook.com/{}/{}?access_token={}".format(
            self.__API_VERSION, user, self.__access_token
        )
