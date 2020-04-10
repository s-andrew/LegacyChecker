import json
from typing import Dict

from redis import Redis


class IdentifierNotFound(Exception):
    pass


class LegalEntityStorage:

    def __init__(self, client: Redis):
        self.client = client
        self.prefix = 'legal.'

    def _make_key(self, identifier):
        return self.prefix + str(identifier)

    def save(self, identifier, payload: dict) -> None:
        self.client.set(self._make_key(identifier), json.dumps(payload))

    def get(self, identifier) -> dict:
        payload_dump = self.client.get(self._make_key(identifier))
        if payload_dump is None:
            raise IdentifierNotFound(f'Identifier {self._make_key(identifier)} not found.')
        return json.loads(payload_dump)

    def get_all(self) -> Dict[str, str]:
        legal_keys = self.client.keys(self._make_key('*'))
        legal_keys_without_prefix = [key[len(self.prefix):] for key in legal_keys]
        dumps = self.client.mget(legal_keys)
        deserialized_payloads = [json.loads(dump) for dump in dumps]
        return dict(zip(legal_keys_without_prefix, deserialized_payloads))

    def clean(self) -> None:
        legal_keys = self.client.keys(self._make_key('*'))
        self.client.delete(*legal_keys)
