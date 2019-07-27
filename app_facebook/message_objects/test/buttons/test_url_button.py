from app_facebook.message_objects.buttons.url_button import UrlButton
from app_facebook.message_objects.test.test_case.message_objects_dummy_case import MessageObjectsDummyCase


class TestUrlButton(MessageObjectsDummyCase):
    def test_to_json(self):
        button = UrlButton('test', 'http://url.com')

        json = button.to_json()
        expected_json = {'title': 'test', 'url': 'http://url.com', 'type': 'web_url'}

        # Assert serialization was correct
        self.assertEqual(json, expected_json)
