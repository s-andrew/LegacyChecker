import datetime
import logging

from flask_restplus import Namespace, Resource, fields

from src.redis_client import redis_client
from src.storage import LegalEntityStorage, IdentifierNotFound
from src.rmsp_fetcher import fetch_from_rmsp

# RMSP_FETCH_TTL = 5 * 60
RMSP_FETCH_TTL = 0

logger = logging.getLogger(__name__)

api = Namespace('legal')


legal_exist_envelope = api.model('Legal Exist Envelope', {
    'identifier': fields.String(),
    'is_exists': fields.Boolean(),
})

identifier_param = api.model('Identifier Param', {
    'identifier': fields.String(required=True),
})


@api.route('/')
class Legal(Resource):

    legal_entities = LegalEntityStorage(client=redis_client)

    @api.marshal_list_with(legal_exist_envelope)
    def get(self):
        return [
            {'identifier': identifier, 'is_exists': payload['is_exists']}
            for identifier, payload in self.legal_entities.get_all().items()
        ]

    @api.expect(identifier_param)
    @api.marshal_with(legal_exist_envelope)
    def post(self):
        identifier = api.payload['identifier']
        now = datetime.datetime.utcnow().timestamp()
        try:
            entity_info = self.legal_entities.get(identifier)
            if now - entity_info['last_update'] > RMSP_FETCH_TTL:
                raise ValueError
            is_exists = entity_info['is_exists']
        except (IdentifierNotFound, ValueError):
            identifier_map = fetch_from_rmsp(identifier)
            logger.error(f'{identifier_map}')
            if identifier_map is None:
                self.legal_entities.save(identifier, {'last_update': now, 'is_exists': False})
                is_exists = False
            else:
                for legal_identifier in identifier_map.values():
                    self.legal_entities.save(legal_identifier, {'last_update': now, 'is_exists': True})
                is_exists = True
        return {'identifier': identifier, 'is_exists': is_exists}

    def delete(self):
        """
        Delete all (just for test).
        """
        self.legal_entities.clean()
