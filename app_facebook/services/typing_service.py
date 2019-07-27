from app_facebook.services.message_dispatcher_service import MessageDispatcher


class TypingService:
    __instance = None

    def __new__(cls):
        if TypingService.__instance is None:
            TypingService.__instance = object.__new__(cls)

            cls.__dispatcher = MessageDispatcher()

        return TypingService.__instance

    def typing_on(self, recipient_id: str):
        message = self.__create_typing_message(recipient_id, True)
        self.__dispatcher.post_message(message, recipient_id)

    def typing_off(self, recipient_id: str):
        message = self.__create_typing_message(recipient_id, False)
        self.__dispatcher.post_message(message, recipient_id)

    def __create_typing_message(self, recipient, turn_on):
        return {
            "recipient": {
                "id": recipient
            },
            "sender_action": "typing_on" if turn_on else "typing_off"
        }
