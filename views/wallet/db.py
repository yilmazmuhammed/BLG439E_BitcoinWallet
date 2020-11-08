from db_models import Transfer, Wallet


def db_send_bitcoin(sender_wallet, receiver_address, amount):
    receiver_wallet = Wallet.get(wallet_address=receiver_address)
    transfer = Transfer(amount=amount, sender_wallet_ref=sender_wallet, receiver_wallet_ref=receiver_wallet)
    ret = sender_wallet.key.send([(receiver_address, amount, 'btc')])
    print(ret)
    print(sender_wallet.key.balance('btc'))
    print(receiver_wallet.key.balance('btc'))
