from gym import Env
from gym.spaces import Discrete
from gym.spaces import Tuple
from gym.spaces import MultiBinary
import numpy as np
import random
from prettytable import PrettyTable
import itertools

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
                bean_growth_no_support = 0.0,
                use_sparse_rewards = False):
        self.harvest_period = harvest_period
        self.fert_cost = fert_cost
        self.corn_growth_no_support = corn_growth_no_support
        self.corn_growth_with_fert = corn_growth_with_fert
        self.corn_growth_with_bean = corn_growth_with_bean
        self.bean_growth_with_support = bean_growth_with_support
        self.bean_growth_no_support = bean_growth_no_support
        self.use_sparse_rewards = use_sparse_rewards
        self.state_space = Tuple((Discrete(2), Discrete(2)))
        self.reset()
        print('=====================================================================')
        print('Environment Details:')
        print('Reward Style:{}'.format('Sparse' if self.use_sparse_rewards else 'Dense'))
        if not self.use_sparse_rewards:
            print('Reward from Corn only: {}'.format(corn_growth_no_support))
            print('Reward from Corn with bean: {}'.format(corn_growth_with_bean))
            print('Reward from Bean when planted too late or too early: {}'.format(bean_growth_no_support))
            print('Reward from Bean when planted after corn is grown enough: {}'.format(bean_growth_with_support))

    def step(self, action):
        done = (self.clock == self.harvest_period)
        self.clock += 1

        step_reward = 0.0
        if self.state[0] == 1:
            self.corn_age += 1
            # TODO : Fertilizer?
            step_reward += self.corn_growth_no_support if self.state[1] == 0 else self.corn_growth_with_bean
        if self.state[1] == 1:
            step_reward += self.bean_growth_with_support if self.bean_got_support else self.bean_growth_no_support

        if action[0] == 1:
            self.state = (1, self.state[1])

        if action[1] == 1:
            self.state = (self.state[0], 1)
            if 4 <= self.corn_age <= 6:
                self.bean_got_support = True
        
        if self.use_sparse_rewards:
            reward = self.sparse_end_reward() if done else 0.0
        else:
            reward = step_reward
        
        return self.get_state(), reward, done, None

    def reset(self):
        self.clock = 0
        self.state = (0, 0)
        self.corn_age = 0
        self.bean_got_support = False
        return self.get_state()

    def sparse_end_reward(self):
        return self.state[0] + (self.state[1] if self.bean_got_support else 0.0)

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

class QTableAgentBase:
    '''
    Common methods for all agent implementations
    '''
    def __init__(self, env):
        self.q_table = {}
        self.env = env

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
                print ('Bean planted at time step {} when the age of corn is {}'.format(time_step, state[2]))
            time_step += 1
            next_state, reward, done, info = self.env.step(action)
            total_reward += reward
            state = next_state
        print ('Total Reward = {}'.format(total_reward))

    def train_and_test(self, epochs):
        print('---------------------------------------------------------------------')
        self.train(epochs)
        self.test()

    def _print_q_table(self):
        states = sorted(self.q_table.keys())
        actions = [(0,0), (0,1), (1,0), (1,1)]
        t = PrettyTable(['state',] + actions)
        for state in states:
            t.add_row([state,] + ['N/A' if a not in self.q_table[state] else self.q_table[state][a] for a in actions])
        print (t)

# Move this to a root location?
class QLearningAgent (QTableAgentBase):
    '''A Q-learning agent that works with openAI gym interface based environment.'''
    def __init__(self, env, learning_rate = 0.1, epsilon = 0.1, discount_rate = 0.9):
        super().__init__(env)
        self.alpha = learning_rate
        self.gamma = discount_rate
        self.epsilon = epsilon

    def train(self, epochs):
        print('Training for Epochs {}, using discount factor {}, epsilon {}, learning rate {}'.format(epochs, self.gamma, self.epsilon, self.alpha))
        lr_decay = 0.9
        epochs_for_decay = 1000
        print ('Decaying the learning rate by {} every {} epochs'.format(lr_decay, epochs_for_decay))
        for epoch in range(1, epochs+1):
            max_diff = 0.0
            state = self.env.reset()
            done = False
            while not done:
                # Why do we need exploitation at all in training phase?
                # I tried commenting the below block of code and instead use random action always,
                # however the results are not good. Though I don't know for certain, it seems to me
                # that the state distribution is not uniform (0, 0, 0) state has a high probability
                # of occurence and it keeps getting updated with actions values from it's following
                # states making it a higher value state and so nothing gets planted at test time.
                if (random.uniform(0, 1) < self.epsilon) or (state not in self.q_table):
                    action = self.env.action_space.sample()
                else:
                    action = max(self.q_table[state].keys(), key=lambda a:self.q_table[state][a])
                # action = self.env.action_space.sample()

                next_state, reward, done, info = self.env.step(action)

                next_state_value = 0.0 if next_state not in self.q_table else max(self.q_table[next_state].values())
                if state not in self.q_table:
                    self.q_table[state] = {}

                oldValue = self.q_table[state].get(action, 0.0)
                self.q_table[state][action] = (1 - self.alpha) * oldValue + self.alpha * (reward + self.gamma * next_state_value)
                diff = np.abs(self.q_table[state][action] - oldValue)
                if (diff > max_diff):
                    max_diff = diff
                state = next_state
            if epoch % epochs_for_decay == (epochs_for_decay-1):
                print ('Maximum update for any state,action pair in epoch {}: {}'.format(epoch, max_diff))
                self.alpha *= 0.9
        print('Training complete. The resulting q_table:')
        self._print_q_table()

class MonteCarloOnPolicyEveryVisitAgent (QTableAgentBase):
    '''
    Implementation for training agent using monte carlo sampling methods.
    On policy implementation and also considers every visit as a candidate sample for updating the value.
    '''
    def __init__(self, env, epsilon = 0.1, discount_rate = 0.9):
        super().__init__(env)
        self.gamma = discount_rate
        self.epsilon = epsilon
        self.visit_counts = {}

    # This method could be part of environment itself but I kept it here as this goes
    # against (?) typical action space design in gym (hmm curious!) and the method was needed
    # for this agent.
    def possible_actions(self, state):
        return list(itertools.product(range(2 - state[0]), range(2 - state[1])))

    def train(self, epochs):
        print('Training for Epochs {}, using discount factor {}, epsilon {}'.format(epochs, self.gamma, self.epsilon))
        policy = {}
        for epoch in range(1, epochs+1):
            state = self.env.reset()
            done = False
            trajectory = [] # list of tuple : (state, action, reward, possible_actions)
            while not done:
                current_state = self.env.get_state() #This is not a generic gym method...
                all_actions = self.possible_actions(current_state)
                action_index = np.random.choice(len(all_actions), p=policy.get(current_state, None))
                action = all_actions[action_index]
                next_state, reward, done, info = self.env.step(action)
                trajectory.append((current_state, action, reward, all_actions))
            G = 0.0
            for t in range(len(trajectory)-1, -1, -1):
                state, action, reward, all_actions = trajectory[t]
                G = self.gamma * G + reward
                self.visit_counts[(state, action)] = 1 + self.visit_counts.get((state, action), 0)
                if state not in self.q_table:
                    self.q_table[state] = {}
                current_estimate = self.q_table[state].get(action, 0)
                self.q_table[state][action] = current_estimate + (G - current_estimate) / self.visit_counts[(state, action)]
                optimal_action = max(self.q_table[state].keys(), key=lambda a:self.q_table[state][a])
                state_policy = []
                for a in all_actions:
                    prob = 1.0 - self.epsilon + self.epsilon / len(all_actions) if a == optimal_action else self.epsilon / len(all_actions)
                    state_policy.append(prob)
                policy[state] = state_policy
        print('Training complete. The resulting q_table:')
        self._print_q_table()

def run(env_spec, agent_spec, epochs=1000):
    env = SingleCellEnv(corn_growth_no_support=env_spec[0],
                        corn_growth_with_bean=env_spec[1],
                        bean_growth_with_support=env_spec[2],
                        bean_growth_no_support=env_spec[3],
                        use_sparse_rewards = True)
    
    agent = MonteCarloOnPolicyEveryVisitAgent(env, epsilon=agent_spec[0], discount_rate=agent_spec[1])
    agent.train_and_test(epochs)

def main():
    run(env_spec = [0.0, 0.0, 0.0, 0.0], agent_spec = [0.2, 0.9], epochs=2)

if __name__ == "__main__":
    main()