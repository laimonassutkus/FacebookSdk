import logging
import traceback

from typing import Optional
from app_facebook.message_objects.reply import Reply
from app_facebook.services.message_dispatcher_service import MessageDispatcher

logr = logging.getLogger(__name__)


class View():
    def __init__(self, reply: Optional[Reply] = None):
        self.reply = reply
        self.message_dispatcher = MessageDispatcher()

    def view(self):
        if self.reply:
            self.message_dispatcher.post_message(message=self.reply.to_json(), recipient_id=self.reply.recipient_id)
        else:
            logr.info('Reply is empty. Not sending a reply.')
