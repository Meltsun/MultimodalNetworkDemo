from dataclasses import dataclass, field
import datetime
from io import BufferedReader
from typing_extensions import Iterable,Callable,TypeVar,Union,Sequence,NamedTuple,cast,Tuple,Dict,TypedDict
from itertools import permutations,product

from schedule.src.iperf_handle import NetworkState,IperfHandle
from schedule.src.utils import logger
from schedule.src.multipath_switch_handle import MultiPathSwitchComposite

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
    def from_net_and_mp_state(net_states:Sequence[NetworkState],mp_state:MultipathState):
        return AllState(
            get_avg_bandwidth(net_states),
            get_percentage_out_of_order(net_states),
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
    return sum_skip_none(networkStates,lambda i:i.lost)/sum_skip_none(networkStates,lambda i:i.total)
    

class Environment:
    stdout:BufferedReader
    iperf_handle:IperfHandle
    max_total_bw:float
    multipath_state:MultipathState#不要直接写这个值，总是使用set_multipath_state，避免造成交换机行为和这个值不一致。

    def __init__(self, max_total_bw:float) -> None:
        self.max_total_bw=max_total_bw
        self.switchs = MultiPathSwitchComposite()
    
    def reset(self,wait_iperf_clients=True) -> AllState:
        self.iperf_handle = IperfHandle(['iperf','-s','-i','1','-p','5000','-u','-e'],logger=logger)
        self.switchs.enable_multipath()
        if wait_iperf_clients:
            input("请启动或重启iperf客户端，并按下回车以继续程序")
        
        self.set_multipath_state(
                MultipathState(
                (5,5,5),
                (1,2,3),
            )
        )
        self.network_states=self.iperf_handle.get_network_states_block()
        state = AllState.from_net_and_mp_state(self.network_states,self.multipath_state)
        self._reseted=True
        return state
    
    def set_multipath_state(self,mp_state:MultipathState)->None:
        self.switchs.set_multipath_state(mp_state.num,mp_state.order)
        self.multipath_state = mp_state

    def step(self,action_index:int):
        if not getattr(self,'_reseted',False):
            raise Exception("必须先执行reset")
        
        action=actions[action_index]
        self.set_multipath_state(
            MultipathState(
                num=cast(Tuple[int,int,int],tuple(i+j for i,j in zip(self.multipath_state.num,action[:3]))),
                order=action[3:]
            )
        )

        new_network_states=self.iperf_handle.monitor_for_seconds(1.1)
        if len(new_network_states) > 0:
            self.network_states=new_network_states

        reward = 0.3 * get_avg_bandwidth(self.network_states)/self.max_total_bw - 0.7 * get_percentage_out_of_order(self.network_states)
        reward *=100

        return AllState.from_net_and_mp_state(self.network_states,self.multipath_state),reward
    
    def close(self) -> None:
        """
        停止iperf和switch。停止后这个实例不能再使用。
        """
        self.pause()
        self.switchs.close()
    
    def pause(self):
        """
        只停止iperf。
        稍后可以用reset恢复。
        """
        self.switchs.disable_multipath()
        self.iperf_handle.close()
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