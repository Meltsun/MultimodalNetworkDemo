"""修改自dqn.py"""
import torch
import collections
import random
import numpy as np
import torch.nn.functional as F
import random
import typing_extensions as typing
from threading import Event

from schedule.src.environment import Environment,actions,AllState
from schedule.src.utils import logger

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = collections.deque(maxlen=capacity)  # define buffer queue, FIFO

    def add(self, state:AllState, action, reward, next_state:AllState):  # add data into buffer
        self.buffer.append((state, action, reward, next_state))
        state_str = np.array_str(np.array(state))
        state_str = state_str.replace('\n', '')
        next_state_str = np.array_str(np.array(next_state))
        next_state_str = state_str.replace('\n', '')
        logger.debug(f"{state_str} {action} {reward} {next_state_str}")

    def sample(self, batch_size):  # get data from buffer, the size of the data is batch_size
        transitions = random.sample(self.buffer, batch_size)
        state, action, reward, next_state = zip(*transitions)
        return np.array(state), action, reward, np.array(next_state)

    def size(self):  # check the size of buffer
        return len(self.buffer)

class Qnet(torch.nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(Qnet, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x1 = F.relu(self.fc1(x))  # use ReLU in layer x to x1
        x2 = self.fc2(x1)
        return x2

class DQN:
    def __init__(self, state_dim, hidden_dim, action_dim, learning_rate, gamma, epsilon, target_update, device):
        self.action_dim = action_dim
        self.q_net = Qnet(state_dim, hidden_dim, self.action_dim).to(device) # Q net
        self.target_q_net = Qnet(state_dim, hidden_dim, self.action_dim).to(device) # target net
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=learning_rate) # use Adam optimizer
        self.gamma = gamma # attenuation factor
        self.epsilon = epsilon # greedy coefficient
        self.target_update = target_update  # update freqency of target Q
        self.count = 0 # counter. store count times
        self.device = device # hardward deployment
        self.action = actions


    def take_action(self, state:AllState, bw, bw1, bw2, bw3)->int:  # get the action index from NN module
        def is_action_ok(action_index) -> bool:
            p1 = state[2] + self.action[action_index][0]
            p2 = state[3] + self.action[action_index][1]
            p3 = state[4] + self.action[action_index][2]
            if p1 >=0 and p2 >= 0 and p3 >=0:
                b1 = bw * p1 / (p1+p2+p3)
                b2 = bw * p2 / (p1+p2+p3)
                b3 = bw * p3 / (p1+p2+p3)
                if b1 <= bw1 and b2 <= bw2 and b3 <= bw3:
                    return True
            return False
        if np.random.random() > self.epsilon:
            state1 = torch.tensor([state], dtype=torch.float).to(self.device)
            action_index = self.q_net(state1).argmax().item()
            if is_action_ok(action_index):
                return typing.cast(int,action_index)
        while True:
            action_index = np.random.randint(self.action_dim)
            if is_action_ok(action_index):
                return typing.cast(int,action_index)

    def update(self, transition_dict): # update NN module, q net, q target(maybe)
        states = torch.tensor(transition_dict['states'], dtype=torch.float).to(self.device)
        actions = torch.tensor(transition_dict['actions']).view(-1, 1).to(self.device)
        rewards = torch.tensor(transition_dict['rewards'], dtype=torch.float).view(-1, 1).to(self.device)
        next_states = torch.tensor(transition_dict['next_states'], dtype=torch.float).to(self.device)
        #dones = torch.tensor(transition_dict['dones'], dtype=torch.float).view(-1, 1).to(self.device)

        q_values = self.q_net(states).gather(1, actions) # get Q from q net according to states
        max_next_q_values = self.target_q_net(next_states).max(1)[0].view(-1, 1) # get maxQ from target q net according to next_states
        #q_targets = rewards + self.gamma * max_next_q_values * (1 - dones)  # calculate q target
        q_targets = rewards + self.gamma * max_next_q_values  # calculate q target
        dqn_loss = torch.mean(F.mse_loss(q_values, q_targets))  # calculte mean square error loss
        self.optimizer.zero_grad() # use gradient optimization
        dqn_loss.backward() # backpropagation update parameters
        self.optimizer.step() # start optimize

        if self.count % self.target_update == 0: # every update q net 10 times, copy q net to tartget q net
            self.target_q_net.load_state_dict(self.q_net.state_dict())  # update
        self.count += 1
        return dqn_loss

# define the hardware deployment of torch, on cpu or gpu(cuda)
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# set the size of buffer
buffer_size = 10000

state_dim = 8
hidden_dim = 128
action_dim = 42
# other parameters of DQN module
lr = 2e-3 # learning rate
gamma = 0.98 # attenuation factor
epsilon = 0.01 # greedy coefficient, 10%->random choose, 90%->choose the max_targetQ
target_update = 10 # update freqency of target Q. After 10 times of Q table update, copy Q table to target Q
# q_target = reward + gamma * max_targetQ
# q' = q + lr * (q_target - q)

# operation parameters
num_episodes = 5 # the total learning times
minimal_size = 10 # the learning interval. Once store 10 data, begin a learning(update q)
batch_size = 9 # the amount of sample in buffer
bw = 8.0
bw1 = 2.7
bw2 = 4.5
bw3 = 6.3


class MultiPathTask:
    def __init__(self) -> None:
        """
        创建实例时会阻塞，直到ssh连接完成。
        请确认iperf服务器已经打开，否则会卡死。
        """
        self.env = Environment(bw) # initial environment
        # build DQN module
        self.agent = DQN(state_dim, hidden_dim, action_dim, lr, gamma, epsilon, target_update, device)
        self.task_stop_event = Event()
        self.isRunning=False
    
    def pause(self):
        self.task_stop_event.set()
        
    def close(self):
        """
        程序结束时请调用，清理ssh连接
        """
        self.env.close()
    
    def __call__(self):
        self.run()
    
    def run(self):
        """
        开启多路径调度
        """
        self.task_stop_event.clear()
        self.isRunning=True
        replay_buffer = ReplayBuffer(buffer_size)
        
        env=self.env
        # start operation. In each episode, the learning need to continue until done=1(ood rate is lower than demand)
        state = env.reset() # initial state. random choose a stored state
        for i_episode in range(num_episodes):
            #done = False # initial done
            logger.debug(f"round {i_episode}")

            while not self.task_stop_event.is_set(): # start learning
                action = self.agent.take_action(state, bw, bw1, bw2, bw3) # get the action index from NN module
                next_state, reward = env.step(action) # calculate parameter to action
                logger.info(f"{next_state},reward")
                replay_buffer.add(state, action, reward, next_state) # store information into buffer
                state = next_state # update state
                # once the size of buffer exceed minimal_size, start learning
                if replay_buffer.size() > (i_episode+1) * minimal_size:
                    b_s, b_a, b_r, b_ns = replay_buffer.sample(batch_size) # get sample data
                    transition_dict = {
                        'states': b_s,
                        'actions': b_a,
                        'next_states': b_ns,
                        'rewards': b_r,
                        #'dones': b_d
                    } # build sample data dictionary
                    dqn_loss = self.agent.update(transition_dict) # update NN network
                    logger.debug(f"{dqn_loss=}")
                    break

            if self.task_stop_event.is_set():
                self.env.pause()
                break
        self.isRunning=False
        
if __name__ == '__main__':
    ...