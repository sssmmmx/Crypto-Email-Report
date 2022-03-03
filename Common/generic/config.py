from Common.generic.api import *
import Common.okex.status_api as status
import Common.okex.Trade_api as Trade
import Common.okex.Account_api as Account
import Common.okex.Public_api as Public
import Common.okex.Market_api as Market
import datetime

okurl = "www.okex.com"


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


StatusAPI = status.StatusAPI(v5_api_key, v5_secret_key, v5_passphrase, False, flag)
tradeAPI = Trade.TradeAPI(v5_api_key, v5_secret_key, v5_passphrase, False, flag)
accountAPI = Account.AccountAPI(v5_api_key, v5_secret_key, v5_passphrase, False, flag)
publicAPI = Public.PublicAPI(v5_api_key, v5_secret_key, v5_passphrase, False, flag)
marketAPI = Market.MarketAPI(v5_api_key, v5_secret_key, v5_passphrase, False, flag)
