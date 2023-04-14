import hashlib
import time
import hmac
import requests
from keys import api_key, secret_key
from binance import Client

client = Client(api_key=api_key, api_secret=secret_key)


class Binance_API():
    api_url = "https://fapi.binance.com"
    api_key = None
    secret_key = None

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def genSignature(self, params):
        param_str = "&".join([f"{k}={v}" for k,v in params.items()])
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        return hash.hexdigest()

    ######################################################################################################################
                                                                        # HTTP Request
    def HTTP_Request(self, endpoint, method, params):
        header = {
            "X-MBX-APIKEY": self.api_key
        }

        params["timestamp"] = int(time.time() * 1000)
        params["signature"] = self.genSignature(params)

        if method == 'GET':
            response = requests.get(url=self.api_url + endpoint, params=params, headers=header)
            print(response.text)

        elif method == 'POST':
            response = requests.post(url=self.api_url + endpoint, params=params, headers=header)
            print(response.text)


        return response.json()

        # return quotes[0][4]

        # print(params["signature"])
        # print(endpoint)
        # print(method)
        # print(params)
######################################################################################################################
    def get_candles(self, symbol, interval, limit=500):
        endpoint = "/fapi/v1/klines"
        method = "GET"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        return self.HTTP_Request(endpoint=endpoint, method=method, params=params)

    ########################################################################################################################
                                # GET POSITION --->  positionAmt
    def position_(self, symbol, request):
        endpoint = 'https://fapi.binance.com/fapi/v2/positionRisk'

        # Define the parameters for the API request
        timestamp = int(time.time() * 1000)
        params = {
            'symbol': symbol,
            'timestamp': timestamp,
            'recvWindow': 5000
        }
        # Generate the API signature
        params_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(secret_key.encode(), params_string.encode(), hashlib.sha256).hexdigest()

        # Add the API signature to the request parameters
        params['signature'] = signature

        # Define the request headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-MBX-APIKEY': api_key
        }

        # Make the API request
        response = requests.get(endpoint, headers=headers, params=params)

        # Parse the response JSON
        data = response.json()

        if request == 'positionAmt':
            return data[0]['positionAmt']

        if request == 'markPrice':
            return data[0]['markPrice']

        print(request, ' = ')
        return data

########################################################################################################################
    # NEW PNL CHECK
    def check_pnl(self):
        try:
            account = client.futures_account()
        except Exception as e:
            print(e.message)
            pass

        for b1 in account['assets']:
            if b1['asset'] == "USDT":
                pnl = float(b1['crossUnPnl'])

        return pnl

########################################################################################################################

    def create_market_order(self, symbol, side, qnt):
        endpoint = "/fapi/v1/order"
        method = "POST"
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": qnt,
            "type": "MARKET"
        }
        return self.HTTP_Request(endpoint=endpoint, method=method, params=params)

########################################################################################################################


    def get_coins_amount_by_usdt(self, symbol, amount):
        coin_price = self.position_(symbol=symbol, request='markPrice')
        coins_amount = (float(amount) / float(coin_price))
        return round(coins_amount, 5)

########################################################################################################################
    """
        Price Precision check for coin amount rounding later on..
    """
    def exchange_info(self, symbol):
        endpoint = "/fapi/v1/exchangeInfo"
        response = requests.get(url=self.api_url + endpoint)
        response = (response.json())
        things = response['symbols']
        for k, v in enumerate(things):
            if v['pair'] == symbol:
                return [v['pricePrecision'], v['quantityPrecision']]
            # elif v['pair'] != symbol:
            #     print('Unknown Pair..')

########################################################################################################################

    """
        Lot size check
    """
    def lot_size_check(self, symbol, usdt):
        lot = usdt / (self.exchange_info(symbol))[0]


