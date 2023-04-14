import hashlib
import hmac
import requests

from api.websocket_data import SocketConn
from api.binance_ import Binance_API
from keys import api_key, secret_key
import time

start_orders = True

if __name__ == "__main__":
    client = Binance_API(api_key=api_key, secret_key=secret_key)

    minus_step = -1
    cycle = True
    first_coin = 'ETHUSDT'
    second_coin = 'BTCUSDT'
    usdt_per_order = 100
    # Price and Lot Precision
    price_precision_1_coin = None
    lot_precision_1_coin = None
    price_precision_2_coin = None
    lot_precision_2_coin = None
########################################################################################################################

    price_from_socket = SocketConn()

    while cycle:


        # CHECK PRECISION FOR SPECIFIC COIN
        print('Precision ☺ ')
        price_precision_1_coin = (client.exchange_info(first_coin))[0]
        lot_precision_1_coin = (client.exchange_info(first_coin))[1]
        price_precision_2_coin = (client.exchange_info(second_coin))[0]
        lot_precision_2_coin = (client.exchange_info(second_coin))[1]
        print(first_coin)
        print(price_precision_1_coin, lot_precision_1_coin)
        print(second_coin)
        print(price_precision_2_coin, lot_precision_2_coin)


        # CHECK QUANTITY BY usdt_per_order


        # OPEN START ORDER
        # global start_orders
        if start_orders:
            print('Open start orders')
            # client.create_market_order(symbol=first_coin, side='BUY', qnt=[price_precision_1_coin, lot_precision_1_coin])
            time.sleep(1)
            # client.create_market_order(symbol=second_coin, side='SELL', qnt=default_qnt)
            start_orders = False

        # GET TOTAL FUTURES PNL
        last_pnl = client.check_pnl()
        time.sleep(1)
        print(f"minus_step is now  {minus_step}")

        # GET POSITION AMOUNT (OPENED POSITION)
        first_coin_open_amount = abs(float(client.position_(symbol=first_coin, request='positionAmt')))
        second_coin_open_amount = abs(float(client.position_(symbol=second_coin, request='positionAmt')))

        #  CHECK IF [pnl < minus_step]
        if last_pnl > minus_step:               # minus_step = -1
            print(f"last_pnl= {last_pnl}")
            # client.create_market_order(symbol=first_coin, side='SELL', qnt=first_coin_open_amount)
            # client.create_market_order(symbol=second_coin, side='BUY', qnt=first_coin_open_amount)
            minus_step -= 1
            print(f"step= {minus_step}")


        # cycle = False

        # print('ETH amount = ' + client.position_(symbol='ETHUSDT', request='positionAmt'))
        # btc_amount = float(client.position_(symbol='BTCUSDT', request='positionAmt'))
        # print('BTC amount = ' , abs(btc_amount))