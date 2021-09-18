# import websocket
# import json
# import sys, getopt
# try:
#     import thread
# except ImportError:
#     import _thread as thread
# from collections import deque

# queue = deque()
# websocket_params = {
#     'type': 'unsubscribe',
#     'product_ids': ['BTC-USD'],
#     'channels': [
#         {
#             'name': 'ticker'
#         }
#     ]
# }

# def on_message(ws, message):
#     queue.append(message['price'])

# def on_error(ws, error):
#     print(error)

# def on_close(ws):
#     print("### closed ###")

# def on_open(ws):
#     def run(*args):
#         ws.send(json.dumps(websocket_params))
#     thread.start_new_thread(run, ())

# def run():
#     print('run')
#     ws.run_forever()

# websocket.enableTrace(True)
# ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com",
#                                 on_open = on_open,
#                                 on_message = on_message,
#                                 on_error = on_error,
#                                 on_close = on_close)
# ws.on_open = on_open

# run()

##########

# class A:
#     def printA(self):
#         print('A')
#         def printB():
#             print('B')
#         printB()
# a = A()
# a.printA()


############

# vals = [1,2,3]
# def get_val():
#     i = 0
#     while True:
#         i = (i+1) % 3
#         yield vals[i]

# count = 0
# for i in get_val():
#     print(i)
#     count += 1
#     if count >= 100:
#         break

#################

import json
import asyncio
import websockets
from websockets import WebSocketServerProtocol

# @asyncio.coroutine
# def hello():
#     websocket_params = {
#         'type': 'subscribe',
#         'product_ids': ['BTC-USD'],
#         'channels': ['ticker']
#     }
#     websocket = yield from websockets.connect('wss://ws-feed.pro.coinbase.com')
#     print('1')
#     yield from websocket.send(json.dumps(websocket_params))
#     print('2')
#     while True:
#         greeting = yield from websocket.recv()
#         print(greeting)

# asyncio.get_event_loop().run_until_complete(hello())



async def hello():
    websocket_params = {
        'type': 'subscribe',
        'product_ids': ['BTC-USD'],
        'channels': ['ticker']
    }
    async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
        await websocket.send(json.dumps(websocket_params))
        while True:
            response = await websocket.recv()
            yield response

async def loop():
    async for i in hello():
        print(i)

asyncio.get_event_loop().run_until_complete(loop())
