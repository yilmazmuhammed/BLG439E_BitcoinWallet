from pony.orm import select

from db_models import BitcoinRequest


def db_add_bitcoin_request(**kwargs):
    return BitcoinRequest(**kwargs)


def db_get_bitcoin_request(bitcoin_request_id):
    return BitcoinRequest.get(id=bitcoin_request_id)

