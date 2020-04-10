from typing import Optional, Dict, Union

import requests
from requests import HTTPError

RMSP_ENDPOINT_URL = 'https://rmsp.nalog.ru/search-proc.json'


def fetch_from_rmsp(identifier: Union[str, int]) -> Optional[Dict[str, str]]:
    params = {
        'mode': 'quick',
        'query': str(identifier),
        'pageSize': '1',
    }
    response = requests.post(RMSP_ENDPOINT_URL, data=params)
    try:
        response.raise_for_status()
        legal_entity_info = response.json()['data'][0]
        return {
            'inn': legal_entity_info['inn'],
            'ogrn': legal_entity_info['ogrn'],
        }
    except (HTTPError, KeyError, IndexError):
        return None
