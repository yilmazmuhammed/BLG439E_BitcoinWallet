from bit import PrivateKeyTestnet
from passlib.handlers.pbkdf2 import pbkdf2_sha256 as hasher

from db_models import WebUser, Wallet
from views.exceptions import EmailAlreadyExist


def db_add_web_user(json_web_user):
    if WebUser.get(email=json_web_user['email']):
        raise EmailAlreadyExist("This email already taken")
    json_web_user['password_hash'] = hasher.hash(json_web_user.pop('password'))
    web_user = WebUser(**json_web_user)
    wallet = db_add_wallet(web_user)

    print("---home page---")
    print(wallet.key)
    print(wallet.key.address)
    print(wallet.wallet_address)
    return web_user


def db_add_wallet(web_user):
    key = PrivateKeyTestnet()
    wallet = Wallet(
        private_key=key.to_wif(),
        wallet_address=key.address,
        web_user_ref=web_user
    )
    return wallet


def get_web_user(**kwargs) -> WebUser:
    ret = WebUser.get(**kwargs)
    return ret
