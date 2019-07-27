from app_facebook.message_objects.buttons.base_button import BaseButton
from app_facebook.message_objects.test.test_case.message_objects_dummy_case import MessageObjectsDummyCase


class TestBaseButton(MessageObjectsDummyCase):
    def test_to_json(self):
        def expected_exception_func():
            # Try to get a next chain
            button = BaseButton()
            button.to_json()

        # Assert that an exception was thrown
        with self.assertRaises(AssertionError):
            expected_exception_func()
