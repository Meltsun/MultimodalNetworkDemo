from fabric import Connection
from invoke import Responder

if __name__ == '__main__':
    host = '219.242.112.215'
    user = 'sinet'
    port = 6182
    password = 'bjtungirc'
    
    conn = Connection(host=host, user=user, port=port, connect_kwargs={'password': password})

    #sudopass = Responder(pattern=r'\[sudo\] password:', response='vagratn\n',)
    # 在远程机器运行命令(用run方法), 并获得返回结果
    # hide 表示隐藏远程机器在控制台的输出, 达到静默的效果
    # 默认 warn是False, 如果远程机器运行命令出错, 那么本地会抛出异常堆栈. 设为True 则不显示这堆栈.
    # result = conn.run('cd /home/vagrant/xuziheng/multipath/', hide=False, warn=False, encoding='utf-8')
    conn.run('cd /home/sinet/xuziheng/')
    result = conn.run('ls')

    # 正常运行时, 信息在 stdout里
    #print('-------- 下面是 stdout 信息')
    #print(result.stdout.strip())

    # 出错时, 信息在 stderr 里
    #print('-------- 下面是 stderr 信息')
    #print(result.stderr.strip())


