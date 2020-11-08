import os
from datetime import datetime

from bit import wif_to_key
from flask_login import UserMixin
from pony.orm import *

db = Database()


class WebUser(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    password_hash = Required(str)
    wallet_ref = Optional('Wallet')
    register_time = Required(datetime, default=lambda: datetime.now())

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return True


class Wallet(db.Entity):
    id = PrimaryKey(int, auto=True)
    private_key = Required(str)
    wallet_address = Optional(str)
    web_user_ref = Required(WebUser)
    diggings_set = Set('Digging')
    sent_transfers_set = Set('Transfer', reverse='sender_wallet_ref')
    received_transfers_set = Set('Transfer', reverse='receiver_wallet_ref')
    bitcoin_requests_set = Set('BitcoinRequest')

    @property
    def key(self):
        return wif_to_key(self.private_key)


class Digging(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Required(int, unsigned=True)
    wallet_ref = Required(Wallet)
    digging_time = Required(datetime, default=lambda: datetime.now())


class Transfer(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Required(float)
    sender_wallet_ref = Required(Wallet, reverse='sent_transfers_set')
    receiver_wallet_ref = Required(Wallet, reverse='received_transfers_set')
    transfer_time = Required(datetime, default=lambda: datetime.now())
    bitcoin_request_ref = Optional('BitcoinRequest')


class BitcoinRequest(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Required(float, default=0)
    min_amount = Required(float, default=0)
    max_count = Required(int, default=0, unsigned=True)
    max_total = Required(float, default=0)
    is_active = Required(bool, default=True)
    wallet_ref = Required(Wallet)
    transfers_set = Set(Transfer)


# PostgreSQL
url = os.getenv("DATABASE_URL")
if url:
    db.bind(provider="postgres", dsn=os.getenv('DATABASE_URL'))
else:
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
# set_sql_debug(True)

db.generate_mapping(create_tables=True)

if __name__ == '__main__':
    pass
