import asyncio
import json
import logging
import time

import aiohttp as aiohttp

from typing import Dict, Union
from django.conf import settings

try:
    # If running in lambda context installing requests lib is not necessary
    # since it is provided from boto3 lib which is also provided by lambda env.
    import requests
except ModuleNotFoundError:
    from botocore.vendored import requests

logr = logging.getLogger(__name__)


class MessageDispatcher:
    __instance = None
    __MAX_REPEATS = 3
    __REPEATED_SLEEP = 0.5

    def __new__(cls):
        if MessageDispatcher.__instance is None:
            MessageDispatcher.__instance = object.__new__(cls)

            cls.__access_token = settings.FACEBOOK_ACCESS_TOKEN

            cls.__endpoint = "https://graph.facebook.com/v2.6/me/messages"
            cls.__headers = {"Content-Type": "application/json"}
            cls.__params = {"access_token": cls.__access_token}

        return MessageDispatcher.__instance

    def post_message(self, message: Dict, recipient_id: str, repeat_index: int = 0):
        if repeat_index >= self.__MAX_REPEATS:
            # Stop recursion
            return

        logr.info("Sending reply to '{}'".format(recipient_id))
        logr.debug("Sending reply to '{}' with payload '{}'".format(recipient_id, json.dumps(message)))

        response = requests.post(**self.__get_kwargs(message))

        if self.__check_response(response, response.text):
            time.sleep(self.__REPEATED_SLEEP)
            self.post_message(message, recipient_id, repeat_index + 1)

    async def post_message_async(self, session: aiohttp.ClientSession, message: Dict, recipient_id: str, repeat_index: int = 0):
        if repeat_index >= self.__MAX_REPEATS:
            # Stop recursion
            return

        logr.info("Sending async reply to '{}'".format(recipient_id))
        logr.debug("Sending async reply to '{}' with payload '{}'".format(recipient_id, json.dumps(message)))

        async with session.post(**self.__get_kwargs(message)) as response:
            if self.__check_response(response, await response.text()):
                asyncio.sleep(self.__REPEATED_SLEEP)
                await self.post_message_async(session, message, recipient_id, repeat_index + 1)

    def __check_response(self, response: Union[requests.Response, aiohttp.ClientResponse], text) -> bool:
        """
        Checks the response from facebook bot api. Returns true if a request should be repeated because response
        indicated an error that can be avoided in the repeated call. Returns false if a request succeeded or
        an error is not recoverable by repeated call.
        """
        try:
            status = response.status_code
        except AttributeError:
            status = response.status

        if status != 200:
            logr.critical(
                'Facebook server did not return status code 200. '
                'Error: error code: \'{}\', error message: \'{}\''.format(str(status), text)
            )

            error_dict = json.loads(text)['error']
            error_code = error_dict['code']

            if (error_code == -1) or (error_code == 1200):
                return True

        return False

    def __get_kwargs(self, message: Dict):
        return {
            'url': self.__endpoint,
            'params': self.__params,
            'headers': self.__headers,
            'data': json.dumps(message).encode('UTF-8')
        }
