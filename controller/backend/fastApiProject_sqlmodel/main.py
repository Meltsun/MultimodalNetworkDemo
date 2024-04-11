from fastapi import FastAPI
import uvicorn, asyncio
from fastapi import FastAPI, HTTPException, Response
from model import Node, NodeType, Link, engine, NodeRead, NodeCreate, NodeUpdate, LinkState, LinkIntCreate, LinkCreate, \
    LinkStateCreat, \
    User, UserLogin, Interface, NetworkPerformance, FirstOne, SecondOne, FirstOneCreate, SecondOneCreate
from sqlmodel import Session, select, SQLModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import hashlib
from congestion import remote_connect
import requests
from ip import client_ips, server_ips
import httpx

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.199.100:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def hash_password(password: str) -> str:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


@app.post("/register")
def register_user(userlogin: UserLogin):
    password = hash_password(userlogin.password)
    # 将用户名和哈希后的密码存储到数据库中的 password_hash 字段中
    # 这里只是示例，实际上需要将用户名和哈希后的密码保存到数据库中
    with Session(engine) as session:
        user = User(username=userlogin.username, password=password)
        session.add(user)
        session.commit()
    return {"message": "注册成功"}


@app.post("/login")
def login(user: UserLogin):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        # 检查用户是否存在
        if not existing_user:
            raise HTTPException(status_code=401, detail="用户名不存在")
        hashed_password_input = hash_password(user.password)
        # 如果用户存在，检查密码是否匹配
        if hashed_password_input != existing_user.password:
            raise HTTPException(status_code=401, detail="密码错误")
        # 返回登录成功
        return {"message": "登录成功"}


@app.get("/topology/", description="获取所有的节点信息，前端生成拓扑")
def get_nodes():
    with Session(engine) as session:
        nodes = session.exec(select(Node)).all()
        links = session.exec(select(Link)).all()
        nodes_data = [{"id": node.id, "label": node.name, "type": node.type.value} for node in
                      nodes]
        links_data = [{"id": link.id, "from": link.node_id_1, "to": link.node_id_2} for link in links]
        return {"nodes": nodes_data, "links": links_data}


@app.post("/node/add", response_model=NodeRead, description="增加节点信息")
def create_node(node: NodeCreate):
    with Session(engine) as session:
        try:
            db_node = Node.model_validate(node)
        except ValueError as e:
            return Response(content=f"错误：{str(e)}", status_code=400)
        session.add(db_node)
        session.commit()
        session.refresh(db_node)
        return Response(content="插入成功", status_code=200)


@app.post("/node/update", response_model=NodeRead, description="更新节点信息")
def update_node(node_id: int, node: NodeUpdate):
    """
    :param node_id: 节点的id号
    :param node: 要更新的节点内容，需要每项内容都进行填写，默认为None
    :return: 更新的节点
    """
    with Session(engine) as session:
        db_node = session.get(Node, node_id)
        if not db_node:
            raise HTTPException(status_code=404, detail="node not found")
        node_data = node.model_dump(exclude_unset=True)
        db_node.sqlmodel_update(node_data)
        session.add(db_node)
        session.commit()
        session.refresh(db_node)
        return db_node


@app.get("/node/{id}", response_model=NodeRead, description="得到某个节点的信息")
def get_one_node(id: int):
    with Session(engine) as session:
        node = session.get(Node, id)
        if not node:
            raise HTTPException(status_code=404, detail="Hero not found")
        return node


@app.delete("/node/{id}", description="删除某个节点的信息")
def delete_node(id: int):
    with Session(engine) as session:
        node = session.get(Node, id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not")
        session.delete(node)
        session.commit()
        return {"ok": True}


@app.get("/interface/{id}", response_model=list[Interface], description="获取某个节点所有的接口信息")
def get_interface(id: int):
    with Session(engine) as session:
        interface = session.exec(select(Interface).where(Interface.node_id == id)).all()
        return interface


@app.get("/link/{id}", description='获取单个链路的信息')
def get_link_state(id: int):
    with Session(engine) as session:
        link = session.get(Link, id)
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        link_state = session.exec(select(LinkState).where(LinkState.link_id == link.id)).first()
        if not link_state:
            raise HTTPException(status_code=404, detail="Link state not found")
        return link_state


@app.post("/link/add")
def create_link(link: LinkCreate):
    with Session(engine) as session:
        db_link = Link.model_validate(link)
        session.add(db_link)
        session.commit()
        session.refresh(db_link)
        return Response(content="插入成功", status_code=200)


@app.get("/high-delay-link", response_model=list[LinkState], description="获取所有的高延迟链路状态信息")
def get_high_delay_link():
    with Session(engine) as session:
        high_delay_links = session.exec(
            select(LinkState).where(LinkState.delay > 100)
        ).all()
        return high_delay_links


@app.delete("/link/{id}", description="获取单个链路的信息")
def get_node(id: int):
    with Session(engine) as session:
        link = session.get(Link, id)
        if not link:
            raise HTTPException(status_code=404, detail="Node not")
        session.delete(link)
        session.commit()
        return {"ok": True}


@app.post("/congestion", description="拥塞接口，使用此接口后更改终端的拥塞算法")
def congestion_controller(congestion_algorithm: str):
    # 设置 SSH 连接参数
    hostname = '219.242.112.215'
    port = 6170
    username = 'sinet'
    password = ''
    command = f'sudo sysctl -w net.ipv4.tcp_congestion_control={congestion_algorithm}'

    # 调用远程连接函数执行命令
    output, error = remote_connect(hostname, port, username, password, command)

    # 返回结果
    return {"output": output, "error": error}


async def send_request(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


async def fetch_data(urls: list[str]):
    tasks = [send_request(url) for url in urls]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses


@app.get("/StartFileReq", description="开启连接")
async def start_file_request():
    # 调用其他服务的接口
    server_port = "5050"
    client_port = "5060"
    # 创建一个异步任务列表
    # 遍历每个服务器IP并创建异步任务
    server_urls = [f"http://{ip}:{server_port}/StartFileReq" for ip in server_ips]
    client_urls = [f"http://{ip}:{client_port}/StartFileReq?amount=25000" for ip in client_ips]
    # server_urls = ["https://www.zhihu.com/", "https://www.baidu.com/"]
    # client_urls = [
    #     "https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9992893171068652083%22%7D&n_type=-1&p_from=-1",
    #     "https://im.qq.com/index/"]

    # 发送异步请求
    server_responses = await fetch_data(server_urls)
    client_responses = await fetch_data(client_urls)

    # 检查响应状态并返回结果
    server_errors = [ip for ip, response in zip(server_ips, server_responses) if isinstance(response, Exception)]
    client_errors = [ip for ip, response in zip(client_ips, client_responses) if isinstance(response, Exception)]

    if server_errors or client_errors:
        error_message = {"err": "Failed to start file request."}
        if server_errors:
            error_message["server_errors"] = server_errors
        if client_errors:
            error_message["client_errors"] = client_errors
        print(error_message)
        return error_message

    # 返回成功消息
    return {"err": ""}


def stop_req(url):
    response = requests.get(url)
    return response.status_code


@app.get("/StopFileReq", description="关闭连接")
def stop_file_req():
    server_errors = []
    client_errors = []
    server_port = "5070"
    client_port = "5080"
    # 关闭服务器的程序
    for ip in server_ips:
        url = f"http://{server_ips}:{server_port}/StopFileReq"
        response_code = stop_req(url)
        if response_code != 200:
            server_errors.append(ip)
    # 关闭客户端的程序
    for ip in client_ips:
        url = f"http://{ip}:{client_port}/StopFileReq"
        response_code = send_request(url)
        if response_code != 200:
            client_errors.append(ip)
    if server_errors or client_errors:
        error_message = {"err": "Failed to stop file request."}
        if server_errors:
            error_message["server_errors"] = server_errors
        if client_errors:
            error_message["client_errors"] = client_errors
        return error_message
    return {"err": ""}


# @app.post("/NetworkPerformance/add", description="添加网络性能数据")
# def add_network_performance(performance: NetworkPerformanceCreate):
#     with Session(engine) as session:
#         db_NetworkPerformance = NetworkPerformance.model_validate(performance)
#         session.add(db_NetworkPerformance)
#         session.commit()
#         session.refresh(db_NetworkPerformance)
#         return Response(content="插入成功", status_code=200)

@app.post("/Firstone/add", description="第一个人发送来的数据，可能仅发送协议信息")
def network_add1(add1: FirstOneCreate):
    with Session(engine) as session:
        db_add1 = FirstOne.model_validate(add1)
        session.add(db_add1)
        session.commit()
        session.refresh(db_add1)
        return Response(content="插入成功", status_code=200)


@app.post("/Secondone/add", description="第二个人发送给我的数据，可能是除了协议之外的所以信息")
def network_add2(add2: SecondOneCreate):
    with Session(engine) as session:
        db_add2 = SecondOne.model_validate(add2)
        session.add(db_add2)
        session.commit()
        session.refresh(db_add2)
        return Response(content="插入成功", status_code=200)


def get_network_performance(session):
    # 查询第一张表和第二张表的所有内容
    first_data = session.exec(select(FirstOne)).all()
    second_data = session.exec(select(SecondOne)).all()
    # 检查数据是否为空
    if not first_data or not second_data:
        raise HTTPException(status_code=404, detail="数据不存在")
    # 将数据合并到第三张表
    for first_entry, second_entry in zip(first_data, second_data):
        existing_entry = session.exec(
            select(NetworkPerformance)
            .where(
                NetworkPerformance.protocol == first_entry.protocol,
                NetworkPerformance.sharpness == second_entry.sharpness,
                NetworkPerformance.buffering == second_entry.buffering,
                NetworkPerformance.delay == second_entry.delay,
                NetworkPerformance.rate == second_entry.rate,
            )
        ).first()
        if not existing_entry:
            network = NetworkPerformance(
                protocol=first_entry.protocol,
                sharpness=second_entry.sharpness,
                buffering=second_entry.buffering,
                delay=second_entry.delay,
                rate=second_entry.rate
            )
            session.add(network)

    session.commit()
    return {"message": "合并成功"}


@app.get("/NetworkPerformance/all", description="获取所有网络性能数据")
def get_all_network_performance():
    with Session(engine) as session:
        get_network_performance(session)
        all_data = session.exec(select(NetworkPerformance)).all()
        return {"data": all_data}


@app.get("/NetworkPerformance/{id}", description="获取单个网络性能数据")
def get_all_network_performance(id: int):
    with Session(engine) as session:
        get_network_performance(session)
        network = session.get(NetworkPerformance, id)
        if not network:
            raise HTTPException(status_code=404, detail="Hero not found")
        return network


@app.post("/get_link_id", description="得到链路的id，需要进一步修改")
def get_link_id(link_data: LinkIntCreate):
    with Session(engine) as session:
        link = (
            session.exec(select(Link).where(
                (Link.node_id_1 == link_data.node_id_1 and Link.node_id_2 == link_data.node_id_2) or
                (Link.node_id_1 == link_data.node_id_2 and Link.node_id_2 == link_data.node_id_1)
            )).first()
        )
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        return {"link_id": link.id}


@app.post("/int/add", description="int包信息传入到数据库")
def create_linkstate(linkstate: LinkStateCreat):
    with Session(engine) as session:
        db_linkstate = LinkState.model_validate(linkstate)
        session.add(db_linkstate)
        session.commit()
        session.refresh(db_linkstate)
        return Response(content="插入成功", status_code=200)


@app.get("/int/sent", description="调用此接口进行int包的发送")
def int_send():
    try:
        # 使用 requests 发送 GET 请求调用接口
        response = requests.get("https://www.baidu.com/")
        # 检查响应状态码，如果不是 200 则抛出 HTTPException
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="调用他人接口失败")
        # 返回成功消息
        return {"message": "Int包发送成功"}
    except Exception as e:
        # 如果发生异常，返回错误消息
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True,
                workers=1)
