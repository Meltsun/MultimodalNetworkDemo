import typing
import fabric
import io
import queue
import typing
import invoke
import logging

class _CommandIO(typing.IO):
    """
    fabric接收一个readable输入，并启动一个线程不断的读取它。如果使用stringIO会导致线程安全问题。
    所以被逼无奈我封装了这么个对象，并使用线程安全的queuq传递数据，并且确保每次输入都以\\n结尾。
    """
    def __init__(self) -> None:
        self.q=queue.Queue()
    def read(self, n: int = -1):
        q=self.q
        all_strings=[]
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

class SimpleSwitchCli:
    """
    用于通过ssh向远程的bmv2 simple switch发送命令。\n
    init会阻塞直到连接完成。\n
    请使用close关闭cli和ssh连接或者直接作为上下文使用。
    """
    def __init__(self,ssh_ip:str,ssh_port:int,user:str,password:str,bmv2_thrift_port:int,logger:typing.Optional[logging.Logger]=None) -> None:
        self.logger = logger if isinstance(logger,logging.Logger) else logging.getLogger("Simple Switch Cli")
        self.command_in=_CommandIO()
        self.stdout=io.StringIO()
        self._lifespan = self._make_lifespan(ssh_ip,ssh_port,user,password,bmv2_thrift_port)
        next(self._lifespan)
    
    def __enter__(self):
        return self

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
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
    
    def _make_lifespan(self,ip:str,port:int,user:str,password:str,bmv2_port:int) -> typing.Generator[None, None, None]:
        connection = fabric.Connection(
            host = host,
            port = port,
            user = user,
            connect_kwargs=dict(password=password)
        )
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
        connection.close()

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

if __name__=="__main__":
    import time
    from utils import config as all_config,logger
    _config= all_config['multipath']['switch']
    host = _config['ssh']['ip']
    port = _config['ssh']['port']
    user = _config['ssh']['user']
    password = _config['ssh']['password']
    bmv2_port = _config['bmv2']['port']

    cli = SimpleSwitchCli(host,port,user,password,bmv2_port,logger)
    cli.send_cmd("help")
    cli.send_cmd("show_actions")
    cli.send_cmd("show_ports")
    cli.send_cmd("show_pvs")
    cli.send_cmd("show_tables")
    time.sleep(1)
    cli.close()
             