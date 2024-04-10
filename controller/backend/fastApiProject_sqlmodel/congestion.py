import paramiko

# 创建 SSH 客户端
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# 定义远程连接函数
def remote_connect(hostname, port, username, password, command):
    try:
        # 连接到服务器
        client.connect(hostname=hostname, port=port, username=username, password=password)
        print("Connected to the server successfully!")

        # 执行命令
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)

        # 输入密码
        stdin.write(password + '\n')
        stdin.flush()

        # 获取命令输出
        output = stdout.read().decode()
        error = stderr.read().decode()

        return output, error

    finally:
        # 关闭 SSH 连接
        stdout.close()
        stderr.close()
        client.close()
