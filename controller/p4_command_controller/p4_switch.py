import abc
import typing_extensions as typing
from abc import ABC
from ipaddress import IPv4Address,IPv4Network
from functools import partial

from p4_command_controller.mac_address import MacAddress

table_entry_params:typing.TypeAlias = typing.Mapping[str,typing.Union[IPv4Address,IPv4Network,MacAddress,int]]

class Register:
    def __init__(self,reset_func:typing.Callable[[],object],set_func:typing.Callable[[int],object]) -> None:
        self.reset = reset_func
        self.set = set_func

class Table:
    def __init__(self,update_entry:typing.Callable[[table_entry_params,str,table_entry_params],object]) -> None:
        self.update_entry = update_entry

class P4Switch(ABC):
    def get_register(self,name:str,*,index:typing.Optional[int]=None)->Register:
        return Register(
            partial(self.reset_register,name),
            typing.cast(typing.Callable[[int], object], partial(self.set_register, name, index=index))
        )
        
    @abc.abstractmethod
    def reset_register(self,name:str):
        ...
    
    @abc.abstractmethod
    def set_register(self,name:str,*,index:typing.Optional[int]=None,value:int):
        """
        设置寄存器的值。
        :param name: 寄存器名，或寄存器列表名
        :param index: 默认为None，如果是寄存器列表请指定序号
        :param value: 设置为此值
        """
        ...
    
    def get_table(self,name:str)->Table:
        return Table(
            partial(self.update_table_entry,name)
        )
    
    @abc.abstractmethod
    def update_table_entry(self,table:str,match_params:table_entry_params,action:str,action_params:table_entry_params={}):
        ...
