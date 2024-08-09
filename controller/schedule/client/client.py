from typing_extensions import Iterable,Callable,TypeVar,Union,Sequence,NamedTuple,cast,Tuple,Dict,TypedDict

from schedule.client.iperf_handle import NetworkState,IperfHandle
from schedule.client.utils import client_logger,iperf_logger

T=TypeVar('T')
U=TypeVar('U',float,int)
def sum_skip_none(container:Iterable[T],value_getter:Callable[[T],Union[None,U]]) -> U:
    sumed = 0
    for i in container:
        value = value_getter(i)
        if value is not None:
            sumed+=value
    return sumed

def get_avg_bandwidth(networkStates:Sequence[NetworkState]) -> float:
    return sum_skip_none(networkStates,lambda i:i.bandwidth)/len(networkStates)

def get_percentage_out_of_order(networkStates:Sequence[NetworkState])->float:
    sumed_oof = sum_skip_none(networkStates,lambda i:i.out_of_order)
    if sumed_oof ==0:
        return 0
    else:
        return sumed_oof/sum_skip_none(networkStates,lambda i:i.total)

class ScheduleClient:
    def __init__(self) -> None:
        self.iperf_handle = IperfHandle(['iperf','-s','-i','1','-p','5000','-u','-e'],client_logger,iperf_logger)

    def monitor_for_seconds(self,duration) -> Tuple[float,float]:
        networkstates = self.iperf_handle.monitor_for_seconds(duration)
        return get_percentage_out_of_order(networkstates),get_avg_bandwidth(networkstates)
        
    def close(self):
        self.iperf_handle.close()