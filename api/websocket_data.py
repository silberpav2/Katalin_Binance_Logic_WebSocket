import api

import json
import websocket
import threading
import traceback
import time


# Websocket threading by Class
class SocketConn(websocket.WebSocketApp):
    def __init__(self, url):
        super().__init__(url=url, on_open=self.on_open)

        self.on_message = lambda ws, msg: self.message(msg)
        self.on_error = lambda ws, e: print('Error', e)
        self.on_close = lambda ws, e: print('Closing')

        self.last_btc = 0.0
        self.last_eth = 0.0


        self.run_forever()

    def on_open(selfself, ws, ):
        print('Websocket was opened')

    def message(self, msg):
        data = json.loads(msg)


        if data['stream'] == 'btcusdt@markPrice':
            self.last_btc = data['data']['p']
            print(self.last_btc)

        if data['stream'] == 'ethusdt@markPrice':
            self.last_eth = data['data']['p']
            print('ETH = ' + self.last_eth)

        # client.position_pnl(symbol='ethusdt')




    def on_error(self, ws, error):
        print('on_error', ws, error)
        print(traceback.format_exc())

threading.Thread(target=SocketConn, args=('wss://fstream.binance.com/stream?streams=ethusdt@markPrice/btcusdt@markPrice',)).start()


# def on_open(ws):
#     sub_msg = {"method": "SUBSCRIBE", "params": ["ethusdt@markPrice"]}
#     ws.send(json.dumps(sub_msg))
#     print("Opened connection")
#
#
# def on_message(ws, message):
#     data = json.loads(message)
#     print(data["p"])
#
#
# url = "wss://fstream.binance.com/ws"
#
# ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message)
# ws.run_forever()
