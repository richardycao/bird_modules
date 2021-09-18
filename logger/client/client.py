import logging

from google.protobuf.json_format import MessageToDict
import asyncio
import grpc
from grpc import aio
import coinbasepro_pb2
import coinbasepro_pb2_grpc

import os

endpoint = os.getenv("INPUT_ENDPOINT", "localhost:50051")

# asynnc grpc client: https://stackoverflow.com/questions/53898185/how-can-i-use-grpc-with-asyncio
async def run():
   async with aio.insecure_channel(endpoint) as channel:
        stub = coinbasepro_pb2_grpc.CoinbaseProStub(channel)
        response = await stub.GetProductTicker(coinbasepro_pb2.GetProductTickerRequest(product_id='BTC-USD'))
        print(MessageToDict(response))
        
        ws_request = coinbasepro_pb2.WebsocketRequest(
            type='subscribe'
        )
        ws_request.product_ids.append('BTC-USD')
        ws_request.channels.append(coinbasepro_pb2.WebsocketChannel(name='ticker'))

        stream = stub.Websocket(ws_request)
        try:
            async for resp in stream.__aiter__():
                print(MessageToDict(resp))
        except grpc.RpcError as e:
            print(e)

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())