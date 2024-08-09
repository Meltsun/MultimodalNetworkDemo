from dataclasses import dataclass, field
import datetime
from io import BufferedReader
from typing_extensions import Iterable,Callable,TypeVar,Union,Sequence,NamedTuple,cast,Tuple,Dict,TypedDict
from itertools import permutations,product
import grpc

from schedule.server.multipath_switch_handle import MultiPathSwitchComposite
from schedule.server.utils import logger,ddqn_config,iperf_config
from schedule import schedule_pb2_grpc,schedule_pb2

@dataclass
class MultipathState:
    num:Tuple[int,int,int]
    order:Tuple[int,int,int]
    time:datetime.datetime=field(default_factory=datetime.datetime.now)

#包含网络状态和多路径调度状态
class AllState(NamedTuple):
    out_of_order:float
    bandwidth:float

    path1_num:int
    path2_num:int
    path3_num:int

    path1_order:int
    path2_order:int
    path3_order:int

    @staticmethod
    def from_net_and_mp_state(avg_network_status:schedule_pb2.AverageNetworkState , mp_state:MultipathState):
        return AllState(
            avg_network_status.out_of_order_rate,
            avg_network_status.bandwidth,
            *mp_state.num,
            *mp_state.order,
        )

delta_actions = ((0,0,0),*permutations((1,0,-1),3))
order_actions = permutations((1,2,3),3)

class Action(NamedTuple):
    path1_delta:int
    path2_delta:int
    path3_delta:int
    path1_order:int
    path2_order:int
    path3_order:int

actions=tuple( Action(*i,*j) for i,j in product(delta_actions,order_actions) )

class Environment:
    stdout:BufferedReader
    grpc_channel:grpc.Channel
    max_total_bw:float
    multipath_state:MultipathState#不要直接写这个值，总是使用set_multipath_state，避免造成交换机行为和这个值不一致。

    def __init__(self, max_total_bw:float) -> None:
        self.max_total_bw=max_total_bw
        self.switchs = MultiPathSwitchComposite()
        self.grpc_channel = grpc.insecure_channel(
            f"{iperf_config.grpc_ip}:{iperf_config.grpc_port}"
        )
        self.grpc_stub=schedule_pb2_grpc.ScheduleClientStub(self.grpc_channel)
    
    def monitor_network(self,duration) -> schedule_pb2.AverageNetworkState:
        return self.grpc_stub.monitor(duration)
    
    def reset(self,wait_iperf_clients=True) -> AllState:
        self.switchs.enable_multipath()
        self.set_multipath_state(
                MultipathState(
                (5,5,5),
                (1,2,3),
            )
        )
        self.avg_network_states=self.monitor_network(1)
        while self.avg_network_states.bandwidth==0:
            self.avg_network_states=self.monitor_network(1)
        state = AllState.from_net_and_mp_state(self.avg_network_states,self.multipath_state)
        self._reseted=True
        return state
    
    def set_multipath_state(self,mp_state:MultipathState)->None:
        self.switchs.set_multipath_state(mp_state.num,mp_state.order)
        self.multipath_state = mp_state

    def step(self,action_index:int) -> Tuple[AllState,float]:
        if not getattr(self,'_reseted',False):
            raise Exception("必须先执行reset")
        
        action=actions[action_index]
        self.set_multipath_state(
            MultipathState(
                num=cast(Tuple[int,int,int],tuple(i+j for i,j in zip(self.multipath_state.num,action[:3]))),
                order=action[3:]
            )
        )

        new_avg_network_states=self.monitor_network(ddqn_config.interval)
        if new_avg_network_states.bandwidth > 0:
            self.avg_network_states=new_avg_network_states

        reward = 0.3 * new_avg_network_states.bandwidth/self.max_total_bw - 0.7 * new_avg_network_states.out_of_order_rate
        reward *=100

        return AllState.from_net_and_mp_state(self.avg_network_states,self.multipath_state),reward
    
    def close(self) -> None:
        """
        停止iperf和switch。停止后这个实例不能再使用。
        """
        self.switchs.close()#close multipath
        def raise_on_call(*args,**kwargs):
            raise Exception("已经关闭")
        self.reset=raise_on_call
        self.grpc_channel.close()
        logger.warn("环境已关闭")
    
    def pause(self):
        """
        只停止iperf。
        稍后可以用reset恢复。
        """
        self.switchs.disable_multipath()#pause multipath
        self._reseted=False


if __name__ == "__main__":
    env=Environment(max_total_bw=10)
    env.reset()
    try:
        while True:
            env.step(int(input()))
            print(env.multipath_state)
    except KeyboardInterrupt:
        env.close()