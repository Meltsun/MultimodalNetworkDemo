import setup_path
# 调用 setup_path 函数
setup_path.setup_path()
import hashlib
from typing import List, Dict
from collections import defaultdict
import requests
import subprocess
import threading
import uvicorn
from fastapi import FastAPI, HTTPException, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func
from congestion import remote_connect
from ip import client_ips, server_ips, servers, PROTOCOL_SINGLE, PROTOCOL_MULTIPATH, data_dict_fake, \
    process_data_history
from model import Node, Link, engine, NodeRead, NodeCreate, NodeUpdate, LinkState, LinkCreate, \
    LinkStateCreat, User, UserLogin, Interface, NetworkPerformance, NetworkPerformanceCreate

# from multipath import multiPathTask


PROTOCOL_DICT = PROTOCOL_SINGLE
state = "场景一"  # 默认值
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


def my_test():
    print("hello world")


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
        links_data = [{"id": link.id, "from": str(link.node_id_1), "to": str(link.node_id_2)} for link in links]
        return {"nodes": nodes_data, "links": links_data}


@app.post("/node/add", response_model=NodeRead, description="增加节点信息")
def create_node(node: NodeCreate):
    with Session(engine) as session:
        try:
            db_node = Node.model_validate(node)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"错误：{str(e)}")
            # return Response(content=f"错误：{str(e)}", status_code=400)
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


@app.get("/node/{id}", description="得到某个节点的信息")
def get_one_node(id: int):
    with Session(engine) as session:
        node = session.get(Node, id)
        if not node:
            raise HTTPException(status_code=404, detail="node not found")
            # error_message = {"state": "fail", "data": "接口未实现该功能"}
            # return JSONResponse(content=error_message, status_code=404)
        node_data = {
            "type": node.type,
            "name": node.name,
            "ip": node.console_ip,
        }
        return node_data


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
        link_state = session.exec(select(LinkState).where(LinkState.link_id == link.id)).all()
        if not link_state:
            raise HTTPException(status_code=404, detail="Link state not found")

        # Sort the link states by create_time in descending order
        sorted_link_state = sorted(link_state, key=lambda x: x.create_time, reverse=True)

        node1 = link.node_id_1
        node2 = link.node_id_2

        # Filter and take the latest entry for each node combination
        latest_link_state = []
        node_combinations = [(node1, node2), (node2, node1)]

        for node_1, node_2 in node_combinations:
            for state in sorted_link_state:
                if state.node_id_1 == node_1 and state.node_id_2 == node_2:
                    state_dict = state.dict(exclude={"id"})
                    state_dict['delay'] = abs(state_dict['delay'])
                    # 只保留3小数
                    state_dict['rate'] = round(state_dict['rate'], 3)
                    latest_link_state.append(state_dict)
                    break

        return latest_link_state


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
        subquery = (
            select(LinkState.link_id, func.max(LinkState.create_time).label('latest_time'))
            .group_by(LinkState.link_id)
            .subquery()
        )

        # 再根据最新时间获取完整记录
        latest_links = session.exec(
            select(LinkState)
            .join(subquery, onclause=(
                    (LinkState.link_id == subquery.c.link_id) &
                    (LinkState.create_time == subquery.c.latest_time)
            ))
        ).all()

        # 过滤延迟大于1500的记录
        high_delay_links = [link for link in latest_links if abs(link.delay) > 1500]
        return high_delay_links


@app.delete("/link/{id}", description="删除单个链路的信息")
def delete_node(id: int):
    with Session(engine) as session:
        link = session.get(Link, id)
        if not link:
            # error_message = {"state": "fail", "data": "接口未实现该功能"}
            # return JSONResponse(content=error_message, status_code=404)
            raise HTTPException(status_code=404, detail="Node not")
        session.delete(link)
        session.commit()
        return {"ok": True}


@app.get("/congestion/{congestion_algorithm}", description="拥塞接口，使用此接口后更改终端的拥塞算法")
def congestion_controller(congestion_algorithm: str):
    congestion_algorithm_lower = congestion_algorithm.lower()
    print(congestion_algorithm_lower)
    # 设置 SSH 连接参数
    hostname = '219.242.112.215'
    ports = [6162, 6164, 6166, 6168, 6180, 6170]
    username = 'sinet'
    password = 'bjtungirc'
    command = f'sudo sysctl -w net.ipv4.tcp_congestion_control={congestion_algorithm_lower}'
    errors = []

    for port in ports:
        result = remote_connect(hostname, port, username, password, command)
        if result['output']:
            print(result['output'])  # 可以在后端输出，也可以通过日志库像loguru
        if result['error']:
            errors.append(f"Port {port}: {result['error']}")
    if errors:
        raise HTTPException(status_code=500, detail="; ".join(errors))
        # 如果没有错误，返回成功信息
    return Response(content="切换成功", status_code=200)


# def send_request(url):
#     response = requests.get(url)
#     return response
#
#
# def fetch_data(urls):
#     threads = []
#     responses = []
#     for url in urls:
#         thread = threading.Thread(target=lambda u: responses.append(send_request(u)), args=(url,))
#         thread.start()
#         threads.append(thread)
#
#     # 等待所有线程完成
#     for thread in threads:
#         thread.join()
#
#     return responses
def send_request(url):
    response = requests.get(url)
    return response


def fetch_data(urls):
    responses = []
    for url in urls:
        response = send_request(url)
        responses.append(response)
    return responses


@app.get("/StartFileReq", description="加大背景流")
def start_file_request():
    # 调用其他服务的接口
    server_port = "8991"
    client_port = "8992"
    # total = 100000
    # 创建一个异步任务列表
    # 遍历每个服务器IP并创建异步任务
    server_urls = [f"http://{ip}:{server_port}/StartFileReq" for ip in server_ips]
    # print(server_urls)

    client_urls = [f"http://{ip}:{client_port}/StartFileReq?amount=20" for ip in client_ips]
    # print(client_urls)
    # server_urls = ["https://zhuanlan.zhihu.com/p/546988581", "https://www.baidu.com/"]
    # client_urls = [
    #     "https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9992893171068652083%22%7D&n_type=-1&p_from=-1",
    #     "https://im.qq.com/index/"]

    # 发送同步请求
    server_responses = fetch_data(server_urls)
    client_responses = fetch_data(client_urls)
    print(server_responses)
    print(client_responses)

    # 新增的判断逻辑
    bad_urls = [url for url, response in zip(client_urls, client_responses) if response.status_code != 200]
    if len(bad_urls) > 10:
        # 如果400的响应超过十次，再发起一次请求
        for _ in range(1):
            second_responses = fetch_data(bad_urls)
            # 再次记录发生错误的url
            bad_urls = [url for url, response in zip(bad_urls, second_responses) if response.status_code != 200]

    # 检查响应状态并返回结果
    # server_errors = [ip for ip, response in zip(server_ips, server_responses) if not response.ok]
    # client_errors = [ip for ip, response in zip(client_ips, client_responses) if not response.ok]
    server_errors = [url for url, response in zip(server_urls, server_responses) if not response.ok]
    client_errors = bad_urls

    if server_errors or client_errors:
        error_message = {"err": "Failed to start file request."}
        if server_errors:
            error_message["server_errors"] = server_errors
        if client_errors:
            error_message["client_errors"] = client_errors
        print(error_message)
    # 返回成功消息
    return {"message": "Requests successfully completed"}


def stop_request(url):
    response = requests.get(url)
    return response.status_code


def attempt_stop(url, attempts=2):
    for _ in range(attempts):
        response_code = stop_request(url)
        if response_code == 200:
            return True  # 成功停止
    return False  # 重试结束依然未成功


@app.get("/StopFileReq", description="缩小背景流")
def stop_file_req():
    server_errors = []
    client_errors = []
    server_port = "8991"
    client_port = "8992"
    # 关闭服务器的程序
    for ip in server_ips:
        url = f"http://{ip}:{server_port}/StopFileReq"
        success1 = attempt_stop(url)
        if not success1:
            server_errors.append(ip)
    # 关闭客户端的程序
    for ip in client_ips:
        url = f"http://{ip}:{client_port}/StopFileReq"
        success2 = attempt_stop(url)
        if not success2:
            client_errors.append(ip)
    if server_errors or client_errors:
        error_message = {"err": "Failed to stop file request."}
        if server_errors:
            error_message["server_errors"] = server_errors
        if client_errors:
            error_message["client_errors"] = client_errors
        return error_message
    return {"message": "Stop successfully completed"}


# @app.post("/NetworkPerformance/add", description="添加网络性能数据")
# def add_network_performance(performance: NetworkPerformanceCreate):
#     with Session(engine) as session:
#         db_NetworkPerformance = NetworkPerformance.model_validate(performance)
#         session.add(db_NetworkPerformance)
#         session.commit()
#         session.refresh(db_NetworkPerformance)
#         return Response(content="插入成功", status_code=200)

# 协议字典


def translate_protocol(protocol_code: str) -> str:
    """将协议编码转换为实际协议名称"""
    return PROTOCOL_DICT.get(protocol_code, "unknown")  # 未知编码默认返回 'unknown'


def update_protocol_dict(new_dict: Dict[str, str]):
    global PROTOCOL_DICT  # 声明为全局变量，这样就能更新它
    PROTOCOL_DICT = new_dict
    return {"message": "协议字典更新成功"}


def process_data(data) -> List[dict]:
    processed_data = []
    # 首先找到BBR协议的尾时延作为参考
    bbr_tail_delay = None
    bbr_congestion_rate = None
    for item in data:
        if item.protocol == 'encc':
            encc_tail_delay = item.tail_delay
            encc_congestion_rate = item.congestion_rate
            break
    for item in data:
        formatted_time = item.create_time.strftime('%Y-%m-%d %H:%M:%S')
        if item.protocol != 'encc':
            if item.tail_delay != 0:
                tail_delay_compare = ((item.tail_delay - encc_tail_delay) / item.tail_delay) * 100
            else:
                tail_delay_compare = 0  # 或者一个表示无法计算的特殊值
            if item.congestion_rate != 0:
                congestion_rate_compare = ((item.congestion_rate - encc_congestion_rate) / item.congestion_rate) * 100
            else:
                congestion_rate_compare = 0  # 或者一个表示无法计算的特殊值
        else:
            tail_delay_compare = 0  # 和自身比较没有改变
            congestion_rate_compare = 0
        processed_item = {
            "protocol": item.protocol,
            "resolution_width": item.resolution_width,
            "resolution_height": item.resolution_height,
            "tail_delay": item.tail_delay,
            "tail_delay_compare": f"{tail_delay_compare:.2f}%",
            "congestion_rate": item.congestion_rate,
            'congestion_rate_compare': f"{congestion_rate_compare:.2f}%",
            "state": item.state,
            "create_time": formatted_time
        }
        processed_data.append(processed_item)
    return processed_data


def get_state() -> str:
    return state


def set_state(new_state: str):
    global state
    state = new_state


@app.post("/Videosituation/add", description="视频参数")
def network_add2(network_performance_data: NetworkPerformanceCreate):
    # 获取当前状态
    current_state = get_state()
    # 检查协议是否为 "0"
    if network_performance_data.protocol == "0":
        return Response(content="协议为 '0'，数据不进行存储", status_code=200)
    # 转换协议编码为名称
    elif network_performance_data.protocol == "24":
        hostname = '219.242.112.215'
        port = 6180
        username = 'sinet'
        password = 'xxxxxxxx'
        command = 'sysctl net.ipv4.tcp_congestion_control'
        result = remote_connect(hostname, port, username, password, command)
        if result.get('error'):
            return Response(content="远程连接失败", status_code=500)
        else:
            congestion_control = result['output'].split('=')[1].strip()
            if congestion_control == 'reno':
                network_performance_data.protocol = "encc"
            else:
                network_performance_data.protocol = congestion_control
            with Session(engine) as session:
                try:
                    db_add = NetworkPerformance.from_orm(network_performance_data)
                    db_add.state = current_state  # 在创建实例之后设置 state
                    session.add(db_add)
                    session.commit()
                    session.refresh(db_add)
                    return Response(content="插入成功", status_code=200)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"错误：{str(e)}")

    network_performance_data.protocol = translate_protocol(network_performance_data.protocol)
    with Session(engine) as session:
        try:
            db_add = NetworkPerformance.from_orm(network_performance_data)
            db_add.state = current_state  # 在创建实例之后设置 state
            session.add(db_add)
            session.commit()
            session.refresh(db_add)
            return Response(content="插入成功", status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"错误：{str(e)}")


@app.get("/NetworkPerformance/latest", description="获取各个场景（8个）网络性能数据最新数据")
def get_all_network_performance():
    with Session(engine) as session:
        all_data = session.exec(select(NetworkPerformance)).all()
        # 按照 state 和 protocol 进行分组
        grouped_data = defaultdict(list)
        for data in all_data:
            key = (data.state, data.protocol)
            grouped_data[key].append(data)
        # 对每个组的数据按照 create_time 进行排序，并保留最新的数据
        latest_data = []
        for key, group in grouped_data.items():
            sorted_group = sorted(group, key=lambda x: x.create_time, reverse=True)
            latest_data.append(sorted_group[0])

        processed_data = process_data(latest_data)
        sorted_processed_data = sorted(processed_data, key=lambda x: x['create_time'], reverse=True)
        return {"data": sorted_processed_data}


@app.get("/NetworkPerformance/history", description="获取所有网络性能数据的历史数据")
def get_all_network_performance():
    with Session(engine) as session:
        all_data = session.exec(select(NetworkPerformance)).all()
        processed_data = process_data_history(all_data)
        return {"data": processed_data}


@app.get("/NetworkPerformance/{id}", description="获取单个网络性能数据")
def get_all_network_performance(id: int):
    with Session(engine) as session:
        network = session.get(NetworkPerformance, id)
        if not network:
            raise HTTPException(status_code=404, detail="Hero not found")
        print(network)

        processed_data = [{"protocol": network.protocol, "resolution_width": network.resolution_width
                              , "resolution_height": network.resolution_height, "tail_delay": network.tail_delay,
                           "congestion_rate": network.congestion_rate}]
        return processed_data


# @app.post("/get_link_id", description="得到链路的id，需要进一步修改")
# def get_link_id(link_data: LinkIntCreate):
#     with Session(engine) as session:
#         link = (
#             session.exec(select(Link).where(
#                 (Link.node_id_1 == link_data.node_id_1 and Link.node_id_2 == link_data.node_id_2) or
#                 (Link.node_id_1 == link_data.node_id_2 and Link.node_id_2 == link_data.node_id_1)
#             )).first()
#         )
#         if not link:
#             raise HTTPException(status_code=404, detail="Link not found")
#         return {"link_id": link.id}


def get_one_link_id(session: Session, node_id_1: int, node_id_2: int) -> int:
    existing_link = session.exec(
        select(Link)
        .where(
            ((Link.node_id_1 == node_id_1) & (Link.node_id_2 == node_id_2)) |
            ((Link.node_id_1 == node_id_2) & (Link.node_id_2 == node_id_1))
        )
    ).first()
    return existing_link.id


@app.post("/int/add", description="int包信息传入到数据库")
def create_linkstate(linkstate: LinkStateCreat):
    with Session(engine) as session:
        link_id = get_one_link_id(session, linkstate.node_id_1, linkstate.node_id_2)
        linkstateAdd = LinkState(node_id_1=linkstate.node_id_1, node_id_2=linkstate.node_id_2, link_id=link_id,
                                 create_time=linkstate.create_time, delay=linkstate.delay, rate=linkstate.rate,
                                 lost=linkstate.lost)
        print(linkstateAdd)
        db_linkstate = LinkState.model_validate(linkstateAdd)
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


# @app.get("/p4/flow/install", description="调用P4流表下发接口")
# def install_p4_flow():
#     try:
#         # 调用他人提供的 P4 流表下发接口的 URL
#         p4_flow_url = "https://www.baidu.com/"
#         # 发送 POST 请求调用他人接口
#         response = requests.get(p4_flow_url)
#         # 检查响应状态码，如果不是 200 则抛出 HTTPException
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail="调用他人接口失败")
#         # 返回成功消息
#         return {"message": "P4 流表下发成功"}
#     except Exception as e:
#         # 如果发生异常，返回错误消息
#         error_message = {"state": "fail", "data": "接口未实现该功能"}
#         return JSONResponse(content=error_message, status_code=404)


@app.get("/multipath", description="多路径")
def multipath(background_tasks: BackgroundTasks):
    set_state("场景二")
    # 暂时省略多路径处理的实现细节，只是更新协议字典
    update = update_protocol_dict(PROTOCOL_MULTIPATH)
    print(update)
    print(PROTOCOL_DICT)
    try:
        result = subprocess.run(["python", "./multipath.py"], capture_output=True, text=True, timeout=25,
                                encoding='utf-8')
        print(result)
        if result.returncode == 0:
            return {"message": "成功运行multipath.py"}
        else:
            return {"error": "运行multipath.py时发生错误"}
    except Exception as e:
        return {"error": f"发生异常：{str(e)}"}
    # if multiPathTask.isRunning:
    #     return {"message": "已经启动，无法再次启动"}
    # else:
    #     background_tasks.add_task(multiPathTask.run)
    #     set_state("场景二")
    #     # 暂时省略多路径处理的实现细节，只是更新协议字典
    #     update = update_protocol_dict(PROTOCOL_MULTIPATH)
    #     print(update)
    #     print(PROTOCOL_DICT)
    #     return {"message": "启动"}


@app.get("/SinglePath", description="单路径")
def singlepath():
    set_state("场景一")
    # 暂时省略多路径处理的实现细节，只是更新协议字典
    update = update_protocol_dict(PROTOCOL_SINGLE)
    print(update)
    print(PROTOCOL_DICT)
    try:
        result = subprocess.run(["python", "./SinglePath.py"], capture_output=True, text=True, timeout=25,
                                encoding='utf-8')
        print(result)
        if result.returncode == 0:
            return {"message": "成功运行SinglePath.py"}
        else:
            return {"error": "运行SinglePath.py时发生错误"}
    except Exception as e:
        return {"error": f"发生异常：{str(e)}"}


def get_data(ip, data_dict):
    port = "8992"
    url = f'http://{ip}:{port}/queryAmountOfConns'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        host_terminal = data.get('hostTerminal')
        amount_of_conns = data.get('amountOfConns')
        amount_of_file_req_conns = data.get('amountOfFileReqConns')

        # 将获取到的数据存储在 data_dict 中
        data_dict[ip] = {
            "hostTerminal": host_terminal,
            "amountOfConns": amount_of_conns,
            "amountOfFileReqConns": amount_of_file_req_conns
        }
    else:
        print(f'Error for IP {ip}: {response.status_code}')


def get_data_threaded(client_ips):
    data_dict = {}
    threads = []
    for ip in client_ips:
        # 创建线程并添加到线程列表
        thread = threading.Thread(target=get_data, args=(ip, data_dict))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()
    print(data_dict)
    return data_dict


def data_handle(communication_terminals, data_dict):
    result_dict = {}
    for item in data_dict:
        communication_terminal1 = data_dict[item]['hostTerminal']  # 假如值为162
        communication_terminal2_list = [x for x in communication_terminals if x != communication_terminal1]
        for communication_terminal2 in communication_terminal2_list:
            # 将通信终端按照升序排列
            terminals = sorted([communication_terminal1, communication_terminal2])
            key_tuple = tuple(terminals)
            active_connections = data_dict[item]["amountOfFileReqConns"] // 5
            total_connections = data_dict[item]['amountOfConns'] // 5
            sleep_connection = total_connections - active_connections

            # 检查键是否已存在，如果存在则累加值，否则直接添加新键值对
            if key_tuple in result_dict:
                result_dict[key_tuple]["active_connections"] += active_connections
                result_dict[key_tuple]["sleep_connections"] += sleep_connection
                result_dict[key_tuple]["total_connections"] += total_connections
            else:
                result_dict[key_tuple] = {
                    "active_connections": active_connections,
                    "sleep_connections": sleep_connection,
                    "total_connections": total_connections
                }
    # print(result_dict)
    return result_dict


@app.get("/test/condition", description="测试系统界面")
def test_condition():
    data_dict = get_data_threaded(client_ips)
    communication_terminals = ["162", "164", "166", "168", "172", "174"]
    ip_mapping = {
        "162": "10.162.162.2",
        "164": "10.164.164.2",
        "166": "10.166.166.2",
        "168": "10.168.168.2",
        "172": "10.172.172.2",
        "174": "10.174.174.2"
    }
    data = data_handle(communication_terminals, data_dict)
    # 转换为前端需要的格式
    formatted_data = []
    for key_tuple, value in data.items():
        formatted_data.append({
            "communication_terminal1": ip_mapping.get(key_tuple[0], key_tuple[0]),
            "communication_terminal2": ip_mapping.get(key_tuple[1], key_tuple[1]),
            "active_connections": value["active_connections"],
            "sleep_connections": value["sleep_connections"],
            "total_connections": value["total_connections"]
        })
    if len(formatted_data) == 0:
        data_fake = data_handle(communication_terminals, data_dict_fake)
        formatted_data_fake = []
        for key_tuple, value in data_fake.items():
            formatted_data_fake.append({
                "communication_terminal1": ip_mapping.get(key_tuple[0], key_tuple[0]),
                "communication_terminal2": ip_mapping.get(key_tuple[1], key_tuple[1]),
                "active_connections": value["active_connections"],
                "sleep_connections": value["sleep_connections"],
                "total_connections": value["total_connections"]
            })
        return formatted_data_fake
    # 返回转换后的数据
    return formatted_data


def Milloin_link():
    # 循环连接服务器并执行命令
    for server in servers:
        output, error = remote_connect(server['hostname'], server['port'], server['username'], server['password'],
                                       server['command'])
        if error:
            print(f"Error executing command on {server['hostname']}: {error}")
        else:
            print(f"Command executed successfully on {server['hostname']}")


if __name__ == '__main__':
    # Milloin_link()
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True,
                workers=1)
