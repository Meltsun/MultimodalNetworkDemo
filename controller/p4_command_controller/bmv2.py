
import typing
import fabric
import io
import queue
import typing_extensions as typing
import invoke
import logging
from ipaddress import IPv4Address

from p4_command_controller.p4_switch import P4Switch,table_entry_params

class _CommandIO(typing.TextIO):
    """
    fabric接收一个readable输入，并启动一个线程不断的读取它。如果使用stringIO会导致线程安全问题。
    所以被逼无奈我封装了这么个对象，并使用线程安全的queuq传递数据，并且确保每次输入都以\\n结尾。
    """
    def __init__(self) -> None:
        self.q:queue.Queue[str]=queue.Queue()
    def read(self, n: int = -1):
        q=self.q
        all_strings:list[str]=[]
        while n != 0 and not q.empty():
            all_strings.append(q.get())
            n -= 1
        return ''.join(all_strings)
    
    def add_cmd(self,cmd:str):
        if cmd:
            for i in cmd:
                self.q.put(i)
            if cmd[-1]!='\n':
                self.q.put('\n')
    
    def send_terminate(self) -> None:
        return self.q.put("\x03")

    def __getattr__(self, name: str):
        raise Exception(f"意外的方法调用，请实现这个方法:{name}")
    
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
        
        self.logger = logger if isinstance(logger,logging.Logger) else logging.getLogger("Simple Switch Cli")
        self.command_in=_CommandIO()
        self.stdout=io.StringIO()
        self._lifespan = self._make_lifespan(ssh_ip,ssh_port,user,password,bmv2_thrift_port)
        if connect_immediately:
            next(self._lifespan)
            self._state = '已连接'
        else:
            self._state = '未连接'
    
    def connect(self) -> None:
        if self._state == '未连接':
            next(self._lifespan)
    
    def close(self) -> None:
        """
        关闭cli，断开ssh连接。
        """
        self.command_in.send_terminate()
        try:
            next(self._lifespan)
        except StopIteration:
            pass
        self.logger.info(f"剩余目标交换机cli输出：\n{self.stdout.getvalue()}")
    
    def _make_lifespan(self,ip:IPv4Address,port:int,user:str,password:str,bmv2_port:int) -> typing.Generator[None, None, None]:
        with fabric.Connection(
            host = ip,
            port = port,
            user = user,
            connect_kwargs=dict(password=password)
        ) as connection:
            p:invoke.runners.Promise=connection.run(
                f"simple_switch_CLI --thrift-port {bmv2_port}",
                asynchronous=True,
                in_stream=self.command_in,
                out_stream=self.stdout,
                pty = True
            )
            yield 
            try:
                p.join()
            except invoke.exceptions.UnexpectedExit:
                self.logger.info("p4 runtime cli 已经关闭。")

    def send_cmd(self,cmd:str):
        """
        发送命令。
        会自动在末尾添加\\n，如果只需要发送一行命令则无需手动添加。
        """
        self.command_in.add_cmd(cmd)
    
    def get_output(self)->str:
        """
        获取所有输出。
        """
        return self.stdout.getvalue()
    
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
