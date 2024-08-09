import grpc
from concurrent import futures

from schedule import schedule_pb2,schedule_pb2_grpc
from schedule.client.client import ScheduleClient

port = 50051

class IperfServer(schedule_pb2_grpc.ScheduleClientServicer):
    def __init__(self) -> None:
        super().__init__()
        self.client = ScheduleClient()
    
    def monitor(self, request:schedule_pb2.MonitorRequest, context)->schedule_pb2.AverageNetworkState:
        out_of_order_rate,bandwidth = self.client.monitor_for_seconds(request.duration)
        return schedule_pb2.AverageNetworkState(bandwidth=bandwidth,out_of_order_rate=out_of_order_rate)
    
    def close(self)->None:
        self.client.close()


def main():
    iperfServer = IperfServer()
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleClientServicer_to_server(iperfServer,server)
    address = f"0.0.0.0:{port}"
    server.add_insecure_port(address)
    server.start()
    print(f"Server started, listening on {address}")
    server.wait_for_termination()
    iperfServer.close()
    
main()