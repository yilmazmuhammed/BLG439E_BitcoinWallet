from db_models import Transfer, Wallet


def db_send_bitcoin(sender_wallet, amount, receiver_address=None, bitcoin_request_ref=None):
    receiver_wallet = bitcoin_request_ref.wallet_ref if bitcoin_request_ref else Wallet.get(
        wallet_address=receiver_address)
    print([(receiver_wallet.wallet_address, amount, 'btc')])
    print(sender_wallet)
    transfer_key = sender_wallet.key.send([(receiver_wallet.wallet_address, amount, 'btc')])
    print(transfer_key)
    # print(sender_wallet.key.balance('btc'))
    # print(receiver_wallet.key.balance('btc'))
    if transfer_key:
        return Transfer(
            amount=amount,
            sender_wallet_ref=sender_wallet,
            receiver_wallet_ref=receiver_wallet,
            bitcoin_request_ref=bitcoin_request_ref,
            transfer_key=transfer_key
        )


def db_get_my_transfers(wallet_id):
    return Transfer.select(lambda t: t.receiver_wallet_ref.id == wallet_id or t.sender_wallet_ref.id == wallet_id).order_by(lambda t: t.transfer_time)
