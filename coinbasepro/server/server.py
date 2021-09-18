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

    # async grpc server: https://stackoverflow.com/questions/38387443/how-to-implement-a-async-grpc-python-server/63020796#63020796
    async def Websocket(self, request, context):
        websocket_params = {
            'type': request.type,
            'product_ids': [pid for pid in request.product_ids],
            'channels': [{
                'name': ch.name,
                'channels': [pid for pid in ch.product_ids]
            } for ch in request.channels]
        }

        async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
            await websocket.send(json.dumps(websocket_params))
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                yield coinbasepro_pb2.WebsocketResponse(
                    type=response['type'],
                    product_id=response['product_id'] if 'product_id' in response else '',
                    time=response['time'] if 'time' in response else '',
                    sequence=response['sequence'] if 'sequence' in response else 0,
                    price=response['price'] if 'price' in response else '',
                    side=response['side'] if 'side' in response else '',
                    trade_id=response['trade_id'] if 'trade_id' in response else 0,
                    last_size=response['last_size'] if 'last_size' in response else '',
                    best_bid=response['best_bid'] if 'best_bid' in response else '',
                    best_ask=response['best_ask'] if 'best_ask' in response else '',
                )

# PR for gRPC graceful shutdown: https://github.com/grpc/grpc/pull/26622
async def serve():
    server = aio.server()
    coinbasepro_pb2_grpc.add_CoinbaseProServicer_to_server(CoinbasePro(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)
    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []

if __name__ == '__main__':
    logging.basicConfig()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()