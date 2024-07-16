
from contextlib import contextmanager
import fabric
import typing_extensions as typing
import logging
from ipaddress import IPv4Address


from p4_command_controller.p4_switch import P4Switch,table_entry_params

class SimpleSwitchHandle(P4Switch):
    """
    用于向远程的bmv2 simple switch发送命令。
    基于ssh而不是p4runtime，性能更差但更灵活。
    """
    
    def __init__(self,*,ssh_ip:IPv4Address,ssh_port:int,user:str,password:str,bmv2_thrift_port:int=9091,logger:typing.Optional[logging.Logger]=None,connect_immediately:bool=True) -> None:
        """
        创建实例时会阻塞直到建立连接。
        请使用close关闭连接。

        :param ssh_ip: bmv2服务器的ip地址，点分十进制
        :param ssh_port: bmv2服务器的ssh端口号
        :param user: ssh登录使用的用户名
        :param password: ssh登录使用的密码
        :param bmv2_thrift_port: bmv2 cli的端口,默认为9091
        :param logger: 使用的logger，如果不传入则会创建一个默认的
        :param connect_immediately: 默认立即连接，可以设置为false以在之后手动连接
        """
        self.deferred_buffer:typing.Optional[typing.List[str]] = None
        self.logger = logger if isinstance(logger,logging.Logger) else logging.getLogger("Simple Switch Cli")
        self._lifespan = self._make_lifespan(ssh_ip,ssh_port,user,password)
        self.bmv2_thrift_port=bmv2_thrift_port
        if connect_immediately:
            self.connect()
    
    def connect(self) -> None:
        if getattr(self,'connection',None) is None:
            self.connection = next(self._lifespan)
    
    def close(self) -> None:
        """
        关闭cli，断开ssh连接。
        """
        if getattr(self,'connection',None) is not None:
            next(self._lifespan)
    
    def _make_lifespan(self,ip:IPv4Address,port:int,user:str,password:str) -> typing.Generator[fabric.Connection, None, None]:
        with fabric.Connection(
            host = str(ip),
            port = port,
            user = user,
            connect_kwargs=dict(password=password)
        ) as connection:
            yield connection
        self.logger.info("p4 runtime cli 已经关闭。")

    @contextmanager
    def make_deferred_executor(self):
        """
        返回一个上下文。
        缓存所有要发送的命令，在最后统一发送
        """
        if self.deferred_buffer is not None:
            raise Exception("不能同时开启两个延迟执行器")
        self.deferred_buffer=[]
        yield
        self.send_cmds(self.deferred_buffer)
        self.deferred_buffer=None
    
    def send_cmd(self,cmd:str):
        """
        发送单个命令。
        会自动在末尾添加\\n，如果只需要发送一行命令则无需手动添加。
        """
        if self.deferred_buffer is not None:
            self.deferred_buffer.append(cmd)
        else:
            result:fabric.Result = self.connection.run(
                f'python3 /home/sinet/P4/behavioral-model/tools/runtime_CLI.py --thrift-port {self.bmv2_thrift_port} <<< \"{cmd}\"',
                timeout=60,
                hide=True
            )
            if len(result.stderr)>0:
                raise Exception(f"命令运行报错:\n{result.stdout}")
            self.logger.debug(result.stdout)
    
    
    def send_cmds(self,cmds:typing.List[str]):
        """
        发送命令。
        会自动在末尾添加\\n，如果只需要发送一行命令则无需手动添加。
        """
        bmv2_cmds='\n'.join(cmds)
        std_in=f"EOF\n{bmv2_cmds}\nEOF"
        cmd=f"python3 /home/sinet/P4/behavioral-model/tools/runtime_CLI.py --thrift-port {self.bmv2_thrift_port} << {std_in}"
        self.logger.debug(f"发送命令 {cmd}")
        result:fabric.Result = self.connection.run(cmd,timeout=60,hide=True)
        
        if len(result.stderr)>0:
            raise Exception(f"命令运行报错:\n{result.stdout}")
        self.logger.debug(f"命令返回结果:\n{result.stdout}")

    @typing.override
    def reset_register(self, name: str):
        return self.send_cmd(f"register_reset {name}")

    @typing.override
    def set_register(self, name: str, *, index: typing.Optional[int] = None, value: int):
        if index is None:
            return self.send_cmd(f"register_write {name} {value}")
        else:
            return self.send_cmd(f"register_write {name} {index} {value}")
        
    @typing.override
    def update_table_entry(self, table: str, match_params: table_entry_params, action: str, action_params: table_entry_params = {}):
        match_s = " ".join(str(i) for i in match_params.values())
        action_params_s = " ".join(str(i) for i in action_params.values())
        self.send_cmd(f"table_add {table} {action} {match_s} => {action_params_s}")

if __name__=="__main__":
    ...
