import typing_extensions as typing

from schedule.src.utils import logger,SwitchConfig,switch_config

from p4_command_controller.bmv2 import SimpleSwitchHandle

class MultiPathSwitchHandle(SimpleSwitchHandle):
    def __init__(self,config:SwitchConfig) -> None:
        self.name=config.name
        super().__init__(
            ssh_ip = config.ssh.ip,
            ssh_port = config.ssh.port,
            user = config.ssh.user,
            password = config.ssh.password,
            bmv2_thrift_port = config.bmv2.port,
            logger = logger
        )
        self.register_indexes=tuple(config.bmv2.register_indexes)
        self.set_register("multipath_ability",index=0,value=1)
        
    def enable_multipath(self):
        self.set_register("transmition_model",index=1,value=1)
    
    def disable_multipath(self):
        self.set_register("transmition_model",index=1,value=0)
        
    def set_multipath_state(self,num:typing.Tuple[int,int,int],order:typing.Tuple[int,int,int]):
        with self.make_deferred_executor():
            register_indexes=self.register_indexes
            for i in ('multipath_count','multipath_initial','multipath_order'):
                self.reset_register(i)
            for i,v in zip(register_indexes,num):
                for name in ('multipath_count','multipath_initial'):
                    self.set_register(name,index=i,value=v)
            for i,v in zip(register_indexes,order):
                self.set_register('multipath_order',index=i,value=v)
    
    def close(self) -> None:
        super().close()
        self.disable_multipath()
        self.logger.warn("bmv2 handle已关闭")

class MultiPathSwitchComposite:
    def __init__(self) -> None:
        logger.info("正在连接bmv2")
        for i in switch_config:
            logger.info(i)
        self.switches = [MultiPathSwitchHandle(i) for i in switch_config]
        logger.info("已连接bmv2")
    
    def _broadcast(self,method:typing.Callable,*args,**kwargs):
        for i in self.switches:
            method(i,*args,**kwargs)
        
    def enable_multipath(self):
        logger.info(f"启动多路径转发")
        self._broadcast(MultiPathSwitchHandle.enable_multipath)
    
    def disable_multipath(self):
        logger.info(f"关闭多路径转发")
        self._broadcast(MultiPathSwitchHandle.disable_multipath)
        
    def set_multipath_state(self,num:typing.Tuple[int,int,int],order:typing.Tuple[int,int,int]):
        logger.info(f"更新多路径状态:{num=},{order=}")
        self._broadcast(MultiPathSwitchHandle.set_multipath_state,num,order)
    
    def close(self):
        self._broadcast(MultiPathSwitchHandle.close)