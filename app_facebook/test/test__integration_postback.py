import json

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase
from app_facebook.chains.chain import Chain
from app_facebook.payloads.payload import Payload
from app_facebook.services.facebook_request_service import FacebookRequestHandler
from app_facebook.test.test_case.dummy_event import DummyEvent


class TestIntegrationPostback(TestCase):
    def test_integration(self):
        json_dict = {
            "entry": [
                {
                    "messaging": [
                        {
                            "timestamp": 1513497365911,
                            "postback": {
                                "payload": 'TEST',
                                "title": 'test'
                            },
                            "recipient": {
                                "id": "1897495093796566"
                            },
                            "sender": {
                                "id": '123'
                            }
                        }
                    ],
                    "id": "1897495093796566",
                    "time": 1513497365911
                }
            ],
            "object": "page"
        }

        event = DummyEvent({ 'title': 'test' })
        chain = Chain(event, 'TEST')

        FacebookRequestHandler().postback_chain_container.chains = [chain]

        json_dump = json.dumps(json_dict).encode()
        request = WSGIRequest({'REQUEST_METHOD': 'POST', 'wsgi.input': len(json_dump)})
        request._body = json_dump

        view = FacebookRequestHandler().handle_post(json_dict)

        expected = json.dumps(DummyEvent.EXPECTED_JSON, sort_keys=True, indent=2)
        actual = json.dumps(view.reply.to_json(), sort_keys=True, indent=2)

        self.assertEqual(expected, actual)
