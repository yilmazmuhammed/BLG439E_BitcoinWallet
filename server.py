import os

from flask import Flask
from flask_login import LoginManager
from pony.flask import Pony

from db_models import WebUser
from views import home_page
from views.authorization.page import register_page, login_page, logout_page
from views.bitcoin_request.page import new_bitcoin_request_page, my_bitcoin_requests_page, bitcoin_request_page
from views.transfer.page import send_bitcoin_page
from views.wallet.page import my_wallet_page

wallet_app = Flask(__name__)
Pony(wallet_app)

wallet_app.secret_key = os.getenv("SECRET_KEY")

# General pages
wallet_app.add_url_rule("/", view_func=home_page)
# Authorization pages
wallet_app.add_url_rule("/register", view_func=register_page, methods=["GET", "POST"])
wallet_app.add_url_rule("/login", view_func=login_page, methods=["GET", "POST"])
wallet_app.add_url_rule("/logout", view_func=logout_page)
# Wallet pages
wallet_app.add_url_rule("/my_wallet", view_func=my_wallet_page)
wallet_app.add_url_rule("/send_bitcoin", view_func=send_bitcoin_page, methods=["GET", "POST"])
# BitcoinRequest pages
wallet_app.add_url_rule("/new_bitcoin_request", view_func=new_bitcoin_request_page, methods=["GET", "POST"])
wallet_app.add_url_rule("/my_bitcoin_requests", view_func=my_bitcoin_requests_page)
wallet_app.add_url_rule("/bitcoin_request/<int:bitcoin_request_id>",
                        view_func=bitcoin_request_page, methods=["GET", "POST"])

lm = LoginManager()
lm.init_app(wallet_app)
lm.login_message_category = 'danger'
lm.login_message = u"Lütfen giriş yapınız."
lm.login_view = "login_page"


@lm.user_loader
def load_user(web_user_id):
    return WebUser.get(id=web_user_id)


if __name__ == '__main__':
    wallet_app.run(debug=True)
