import json

from typing import Dict


class Payload:
    PAYLOAD_KEY = 'uid'

    def __init__(self, unique_id: str, payload_dict: Dict[str, str] = {}):
        self.payload_dict = payload_dict
        self.unique_id = unique_id

    def __str__(self):
        return self.unique_id + str(self.payload_dict)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.payload_dict == other.payload_dict and self.unique_id == other.unique_id

    def serialize(self) -> str:
        d = self.payload_dict.copy()
        d[self.PAYLOAD_KEY] = self.unique_id

        return json.dumps(d)

    @staticmethod
    def deserialize(payload: str) -> 'Payload':
        """
        Deserializes payloads.
        """
        payload = json.loads(payload)

        uid = payload[Payload.PAYLOAD_KEY]
        del payload[Payload.PAYLOAD_KEY]

        return Payload(unique_id=uid, payload_dict=payload)

    @staticmethod
    def match(payload: str, uid: str) -> bool:
        """
        By the given serialized payloads, determine if it matches uid.
        """
        return json.loads(payload)[Payload.PAYLOAD_KEY] == uid
