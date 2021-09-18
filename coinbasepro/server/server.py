import coinbasepro as cbp
import asyncio
import websockets
from websockets import WebSocketServerProtocol
import json

from concurrent import futures
import logging

import grpc
from grpc import aio
import coinbasepro_pb2
import coinbasepro_pb2_grpc

class CoinbasePro(coinbasepro_pb2_grpc.CoinbaseProServicer):
    def __init__(self):
        self.client = cbp.PublicClient()
    
    def GetProductTicker(self, request, context):
        response = self.client.get_product_ticker(request.product_id)
        return coinbasepro_pb2.GetProductTickerResponse(
            trade_id = response['trade_id'],
            price = str(response['price']),
            size = str(response['size']),
            bid = str(response['bid']),
            ask = str(response['ask']),
            volume = str(response['volume']),
            time = str(response['time'])
        )
    # https://stackoverflow.com/questions/53898185/how-can-i-use-grpc-with-asyncio
    # async def Websocket(self, request, context):
    #     websocket_params = {
    #         'type': request.type,
    #         'product_ids': [pid.product_id for pid in request.product_ids],
    #         'channels': [{
    #             'name': ch.name,
    #             'channels': [pid.product_id for pid in ch.product_ids]
    #         } for ch in request.channels]
    #     }

    #     while True:
    #         yield coinbasepro_pb2.WebsocketResponse(
    #             type='test_type'
    #         )
        # async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
        #     await websocket.send(json.dumps(websocket_params))
        #     while True:
        #         response = await websocket.recv()
        #         print(response)
        #         yield coinbasepro_pb2.WebsocketResponse(
        #             type='hello'
        #         )

async def serve():
    server = aio.server()
    coinbasepro_pb2_grpc.add_CoinbaseProServicer_to_server(CoinbasePro(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(serve())