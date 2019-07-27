from app_facebook.message_objects.buttons.quick_button import QuickButton
from app_facebook.message_objects.test.test_case.message_objects_dummy_case import MessageObjectsDummyCase


class TestQuickkButton(MessageObjectsDummyCase):
    def test_to_json(self):
        button = QuickButton('test', 'payload', 'https://image.com')

        json = button.to_json()
        expected_json = {'payload': 'payload', 'title': 'test', 'image_url': 'https://image.com', 'content_type': 'text'}

        # Assert serialization was correct
        self.assertEqual(json, expected_json)
