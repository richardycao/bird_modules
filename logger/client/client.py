import logging

from google.protobuf.json_format import MessageToDict
import grpc
import coinbasepro_pb2
import coinbasepro_pb2_grpc

import os

endpoint = os.getenv("INPUT_ENDPOINT", "localhost:50051")

def run():
    with grpc.insecure_channel(endpoint) as channel:
        stub = coinbasepro_pb2_grpc.CoinbaseProStub(channel)
        response = stub.GetProductTicker(coinbasepro_pb2.GetProductTickerRequest(product_id='BTC-USD'))
        print(MessageToDict(response))


if __name__ == '__main__':
    logging.basicConfig()
    run()