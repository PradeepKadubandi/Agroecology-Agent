from gym import Env
from gym.spaces import Discrete
from gym.spaces import Tuple
from gym.spaces import MultiBinary
import numpy as np
import random
from prettytable import PrettyTable

class SingleCellEnv(Env):
    '''
    Model a single cell where corn and bean can be planted.
    If a bean is ever planted, it follows the rewards for corn from bean and bean from corn.
    If bean is never planted, it follows the rewards from fertilizer (TODO)
    taking the corn and growth and fert cost into account.
    '''

    def __init__(self,
                harvest_period = 30,
                fert_cost = 0.0,
                corn_growth_no_support = 0.6,
                corn_growth_with_fert = 1.0,
                corn_growth_with_bean = 0.9,
                bean_growth_with_support = 0.5,
                bean_growth_no_support = 0.0):
        self.harvest_period = harvest_period
        self.fert_cost = fert_cost
        self.corn_growth_no_support = corn_growth_no_support
        self.corn_growth_with_fert = corn_growth_with_fert
        self.corn_growth_with_bean = corn_growth_with_bean
        self.bean_growth_with_support = bean_growth_with_support
        self.bean_growth_no_support = bean_growth_no_support
        self.state_space = Tuple((Discrete(2), Discrete(2)))
        self.reset()
        print('=====================================================================')
        print('Environment Details:')
        print('Reward Style:Dense') # TODO: Need to see what happens if we keep track of growth and return the reward at end of episode i.e, sparse reward.
        print('Reward from Corn only: {}'.format(corn_growth_no_support))
        print('Reward from Corn with bean: {}'.format(corn_growth_with_bean))
        print('Reward from Bean when planted too late or too early: {}'.format(bean_growth_no_support))
        print('Reward from Bean when planted after corn is grown enough: {}'.format(bean_growth_with_support))

    def step(self, action):
        done = (self.clock == self.harvest_period)
        self.clock += 1

        reward = 0.0
        if self.state[0] == 1:
            self.corn_age += 1
            # TODO : Fertilizer?
            reward += self.corn_growth_no_support if self.state[1] == 0 else self.corn_growth_with_bean
        if self.state[1] == 1:
            reward += self.bean_growth_with_support if self.bean_got_support else self.bean_growth_no_support

        if action[0] == 1:
            self.state = (1, self.state[1])

        if action[1] == 1:
            self.state = (self.state[0], 1)
            if 4 <= self.corn_age <= 6:
                self.bean_got_support = True
        
        return self.get_state(), reward, done, None

    def reset(self):
        self.clock = 0
        self.state = (0, 0)
        self.corn_age = 0
        self.bean_got_support = False
        return self.get_state()

    def close(self):
        pass

    def render(self, mode):
        print ('state: {}'.format(self.state))

    def seed(self, seed=None):
        return []

    def get_state(self):
        # return self.state
        return self.state + (self.corn_age,)

    @property
    def action_space(self):
        first = Discrete(2 - self.state[0]) # For state value 0, we have 2 choices 0 and 1. For state value 1 we have only one choice.
        second = Discrete(2 - self.state[1])
        return Tuple((first, second))

# Move this to a root location?
class QLearningAgent:
    '''A Q-learning agent that works with openAI gym interface based environment.'''
    def __init__(self, env, learning_rate = 0.1, epsilon = 0.1, discount_rate = 0.9):
        self.q_table = {}
        self.env = env
        self.alpha = learning_rate
        self.gamma = discount_rate
        self.epsilon = epsilon

    def train(self, epochs):
        print('Training for Epochs {}, using discount factor {}, epsilon {}, learning rate {}'.format(epochs, self.gamma, self.epsilon, self.alpha))
        for _ in range(epochs):
            state = self.env.reset()
            done = False
            while not done:
                if (random.uniform(0, 1) < self.epsilon) or (state not in self.q_table):
                    action = self.env.action_space.sample()
                else:
                    action = max(self.q_table[state].keys(), key=lambda a:self.q_table[state][a])

                next_state, reward, done, info = self.env.step(action)

                next_state_value = 0.0 if next_state not in self.q_table else max(self.q_table[next_state].values())
                if state not in self.q_table:
                    self.q_table[state] = {}

                self.q_table[state][action] = (1 - self.alpha) * self.q_table[state].get(action, 0.0) + self.alpha * (reward + self.gamma * next_state_value)
                state = next_state
        print('Training complete. The resulting q_table:')
        self.__print_q_table()

    def test(self):
        print('Test Run')
        state = self.env.reset()
        done = False
        total_reward = 0.0
        time_step = 0
        while not done:
            action = max(self.q_table[state].keys(), key=lambda a:self.q_table[state][a])
            if action[0] == 1 and state[0] == 0:
                print ('Corn planted at time step {}'.format(time_step))
            if action[1] == 1 and state[1] == 0:
                print ('Bean planted at time step {}'.format(time_step))
            time_step += 1
            next_state, reward, done, info = self.env.step(action)
            total_reward += reward
            state = next_state
        print ('Total Reward = {}'.format(total_reward))

    def train_and_test(self, epochs):
        print('---------------------------------------------------------------------')
        self.train(epochs)
        self.test()

    def __print_q_table(self):
        states = sorted(self.q_table.keys())
        actions = [(0,0), (0,1), (1,0), (1,1)]
        t = PrettyTable(['state',] + actions)
        for state in states:
            t.add_row([state,] + ['N/A' if a not in self.q_table[state] else self.q_table[state][a] for a in actions])
        print (t)

def main():
    env_specifications = [[0.5, 1.0, 0.7, 0.0],
                          [0.5, 1.0, 1.0, 0.0],
                          [2.0, 1.0, 0.5, 0.0],
                          [2.0, 1.0, 1.0, 0.0],
                          [0.5, 1.0, 1.5, 0.0]]
    for spec in env_specifications:
        env = SingleCellEnv(corn_growth_no_support=spec[0], corn_growth_with_bean=spec[1], bean_growth_with_support=spec[2], bean_growth_no_support=spec[3])
        for gamma in [0.5, 0.9, 1.0]:
            agent = QLearningAgent(env, discount_rate=gamma)
            agent.train_and_test(1000)

if __name__ == "__main__":
    main()