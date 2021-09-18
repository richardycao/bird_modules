import logging

from google.protobuf.json_format import MessageToDict
import asyncio
import grpc
from grpc import aio
import coinbasepro_pb2
import coinbasepro_pb2_grpc

import os

endpoint = os.getenv("INPUT_ENDPOINT", "localhost:50051")

def run():
   with grpc.insecure_channel(endpoint) as channel:
        stub = coinbasepro_pb2_grpc.CoinbaseProStub(channel)
        response = stub.GetProductTicker(coinbasepro_pb2.GetProductTickerRequest(product_id='BTC-USD'))
        print(MessageToDict(response))
        
        # ws_request = coinbasepro_pb2.WebsocketRequest()
        # ws_request.type = 'subscribe'
        # pid1 = ws_request.product_ids.add()
        # channel1 = ws_request.channels.add()
        # pid1 = coinbasepro_pb2.WebsocketProductId(product_id='BTC-USD')
        # channel1 = coinbasepro_pb2.WebsocketChannel(name='ticker')

        # stream = await stub.Websocket(ws_request)
        # try:
        #     async for resp in stream.__aiter__():
        #         print(resp.type)
        # except grpc.RpcError as e:
        #     print(e)

        # async def loop():
        #     stream = stub.Websocket(ws_request)
        #     try:
        #         async for resp in stream.__aiter__():
        #             print(resp.type)
        #     except grpc.RpcError as e:
        #         print(e)
        # asyncio.run(loop())

        # stream = await stub.Websocket(ws_request)
        # try:
        #     async for resp in stream.__aiter__():
        #         print(resp.type)
        # except grpc.RpcError as e:
        #     print(e)

        # await for i in stub.Websocket(ws_request):
        #     print(i.type)
        # async def loop():
        #     x = stub.Websocket(ws_request)
        #     async for i in x:
        #         print(i.type)
        #     else:
        #         print('else')
        # asyncio.run(loop())

        # async def loop():
        #     async for i in stub.Websocket(coinbasepro_pb2.WebsocketRequest(
        #         type='subscribe',
        #         product_ids=[coinbasepro_pb2.WebsocketProductId(
        #             product_id='BTC-USD')
        #         ],
        #         channels=[coinbasepro_pb2.WebsocketChannel(
        #             name='ticker'
        #         )]
        #     )):
        #         print(i)
        # asyncio.get_event_loop().run_until_complete(loop())
        # asyncio.get_event_loop().run_until_complete(
        #     stub.Websocket(coinbasepro_pb2.WebsocketRequest(
        #         type='subscribe',
        #         product_ids=[coinbasepro_pb2.WebsocketProductId(
        #             product_id='BTC-USD')
        #         ],
        #         channels=[coinbasepro_pb2.WebsocketChannel(
        #             name='ticker'
        #         )]
        #     ))
        # )


        # for resp in stub.WebsocketRequest({
        #     'type': 'subscribe',
        #     'product_ids': ['BTC-USD'],
        #     'channels': [
        #         {
        #             'name': 'ticker'
        #         }]}):
        #     print('hi')
        #     print(resp.product_id)
            # print(MessageToDict(resp))

if __name__ == '__main__':
    logging.basicConfig()
    run()