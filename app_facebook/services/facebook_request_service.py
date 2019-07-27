import json
import logging

from typing import Dict, Union, List
from django.conf import settings
from app_facebook.services.typing_service import TypingService
from app_facebook.chain_containers.messages_chain_container import MessagesChainContainer
from app_facebook.chain_containers.postback_chain_container import PostbackChainContainer
from app_facebook.chain_containers.quick_reply_chain_container import QuickReplyChainContainer
from app_facebook.payloads.payload import Payload
from app_facebook.services.message_dispatcher_service import MessageDispatcher
from app_facebook.view import View

logr = logging.getLogger(__name__)


class FacebookRequestHandler:
    __instance = None

    def __new__(cls):
        if FacebookRequestHandler.__instance is None:
            FacebookRequestHandler.__instance = object.__new__(cls)

            cls.__dispatcher = MessageDispatcher()

            cls.quick_reply_chain_container = QuickReplyChainContainer()
            cls.postback_chain_container = PostbackChainContainer()
            cls.message_chain_container = MessagesChainContainer()

        return FacebookRequestHandler.__instance

    def handle_get(self, hub_verify_token: str) -> None:
        verify_token = hub_verify_token
        assert verify_token, 'Verify token from the request not given'
        internal_verify_token = settings.FACEBOOK_VERIFY_TOKEN
        assert internal_verify_token, 'Verify token not set in environment'

        match = internal_verify_token == verify_token

        if not match:
            raise ValueError('Tokens do not match')

    def handle_post(self, payload: Dict) -> Union[View, List[View]]:
        logr.info('Processing payload: {}'.format(json.dumps(payload)))

        if payload["object"] == "page":
            for entry in payload["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        # We got a quick reply (quick reply button was pressed).
                        if messaging_event["message"].get("quick_reply"):
                            return self.__process_quick_reply(messaging_event)
                        # We got a simple text message.
                        if messaging_event['message'].get('text'):
                            return self.__process_text_message(messaging_event)
                        # We got a sticker.
                        if messaging_event['message'].get('sticker_id'):
                            return self.__process_sticker_message(messaging_event)
                        else:
                            logr.warning("Could not handle the message from the user. Its not text nor payloads. Event details: '{}'".format(messaging_event))
                            return View()

                    # We got a post back (e.g. get started)
                    elif messaging_event.get("postback"):
                        return self.__process_postback_message(messaging_event)

                    else:
                        # Do not log since it floods logs
                        # logr.warning("Received an unknown event: '{}'".format(messaging_event))
                        return View()

    def __process_postback_message(self, messaging_event: Dict) -> Union[View, List[View]]:
        user_fb_id = messaging_event["sender"]["id"]
        payload = messaging_event["postback"]["payload"]
        payload_title = messaging_event["postback"]["title"]
        payload = Payload(payload, { 'title': payload_title })

        TypingService().typing_on(user_fb_id)

        logr.info("Processing received POSTBACK '{}' from '{}'.".format(payload.serialize(), user_fb_id))
        view = self.postback_chain_container.get_chain().raise_event(payload.serialize(), user_fb_id).raise_view()

        TypingService().typing_off(user_fb_id)

        return view

    def __process_quick_reply(self, messaging_event: Dict) -> Union[View, List[View]]:
        user_fb_id = messaging_event["sender"]["id"]
        payload = messaging_event["message"]["quick_reply"]['payload']

        TypingService().typing_on(user_fb_id)

        logr.info("Processing received QUICK-REPLY '{}' from '{}'.".format(user_fb_id, payload))
        view = self.quick_reply_chain_container.get_chain().raise_event(payload, user_fb_id).raise_view()

        TypingService().typing_off(user_fb_id)

        return view

    def __process_text_message(self, messaging_event: Dict) -> Union[View, List[View]]:
        user_fb_id = messaging_event["sender"]["id"]
        payload = messaging_event["message"]["text"]
        payload = Payload('MESSAGE', { 'text': payload })

        TypingService().typing_on(user_fb_id)

        logr.info("Processing received MESSAGE '{}' from '{}'.".format(payload, user_fb_id))
        view = self.message_chain_container.get_chain().raise_event(payload.serialize(), user_fb_id).raise_view()

        TypingService().typing_off(user_fb_id)

        return view

    def __process_sticker_message(self, messaging_event: Dict) -> Union[View, List[View]]:
        user_fb_id = messaging_event["sender"]["id"]
        sticker_id = messaging_event["message"]["sticker_id"]
        payload = Payload('STICKER', { 'sticker_id': sticker_id })

        TypingService().typing_on(user_fb_id)

        logr.info("Processing received STICKER '{}' from '{}'.".format(payload, user_fb_id))
        view = self.message_chain_container.get_chain().raise_event(payload.serialize(), user_fb_id).raise_view()

        TypingService().typing_off(user_fb_id)

        return view
