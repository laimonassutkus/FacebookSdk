from app_facebook.message_objects.buttons.postback_button import PostbackButton
from app_facebook.message_objects.test.test_case.message_objects_dummy_case import MessageObjectsDummyCase


class TestPostbackButton(MessageObjectsDummyCase):
    def test_to_json(self):
        button = PostbackButton('test', 'payload')

        json = button.to_json()
        expected_json = {'payload': 'payload', 'title': 'test', 'type': 'postback'}

        # Assert serialization was correct
        self.assertEqual(json, expected_json)
