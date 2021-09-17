import coinbasepro as cbp

from concurrent import futures
import logging

import grpc
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    coinbasepro_pb2_grpc.add_CoinbaseProServicer_to_server(CoinbasePro(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()