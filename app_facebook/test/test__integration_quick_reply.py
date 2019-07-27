import json

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase
from app_facebook.chains.chain import Chain
from app_facebook.payloads.payload import Payload
from app_facebook.services.facebook_request_service import FacebookRequestHandler
from app_facebook.test.test_case.dummy_event import DummyEvent


class TestIntegrationQuickReply(TestCase):
    def test_integration(self):
        payload = Payload('TEST', DummyEvent.EXPECTED_PAYLOAD_DICT)

        json_dict = {
            "entry": [
                {
                    "messaging": [
                        {
                            "timestamp": 1501777122213,
                            "message": {
                                "text": "Test message",
                                "mid": "mid.$cAAbnMLPVyFxj2imbpVdqORTv6CLT",
                                "seq": 426689,
                                "quick_reply": {
                                    "payload": payload.serialize()
                                }
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
                    "time": 1501777122614
                }
            ],
            "object": "page"
        }

        event = DummyEvent()
        chain = Chain(event, 'TEST')

        FacebookRequestHandler().quick_reply_chain_container.chains = [chain]

        json_dump = json.dumps(json_dict).encode()
        request = WSGIRequest({'REQUEST_METHOD': 'POST', 'wsgi.input': len(json_dump)})
        request._body = json_dump

        view = FacebookRequestHandler().handle_post(json_dict)

        expected = json.dumps(DummyEvent.EXPECTED_JSON, sort_keys=True, indent=2)
        actual = json.dumps(view.reply.to_json(), sort_keys=True, indent=2)

        self.assertEqual(expected, actual)
