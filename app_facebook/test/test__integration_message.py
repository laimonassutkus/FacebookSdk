import json

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase
from app_facebook.chains.chain import Chain
from app_facebook.services.facebook_request_service import FacebookRequestHandler
from app_facebook.test.test_case.dummy_event import DummyEvent
from app_facebook.test.test_case.dummy_message_event import DummyMessageEvent


class TestIntegrationMessage(TestCase):
    def test_integration(self):
        json_dict = {
            "entry": [
                {
                    "messaging": [
                        {
                            "timestamp": 1513500364748,
                            "message": {
                                "text": DummyMessageEvent.EXPECTED_MESSAGE,
                                "mid": "mid.$cAAbnMLPVyFxmlOwXzFgY6bZ7H7a4",
                                "seq": 479412
                            },
                            "recipient": {
                                "id": "1897495093796566"
                            },
                            "sender": {
                                "id": "1444250085633761"
                            }
                        }
                    ],
                    "id": "1897495093796566",
                    "time": 1513500365490
                }
            ],
            "object": "page"
        }

        event = DummyMessageEvent()
        chain = Chain(event, 'MESSAGE')

        FacebookRequestHandler().message_chain_container.chains = [chain]

        json_dump = json.dumps(json_dict).encode()
        request = WSGIRequest({'REQUEST_METHOD': 'POST', 'wsgi.input': len(json_dump)})
        request._body = json_dump

        view = FacebookRequestHandler().handle_post(json_dict)

        expected = json.dumps(DummyEvent.EXPECTED_JSON, sort_keys=True, indent=2)
        actual = json.dumps(view.reply.to_json(), sort_keys=True, indent=2)

        self.assertEqual(expected, actual)
