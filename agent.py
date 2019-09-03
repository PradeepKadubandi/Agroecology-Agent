import numpy as np
import random
import Node
import numpy as np
def explore_strategy(actions):
    """
    :return: action index from the q_table
    """
    return random.choice(actions)


class QLearningAgent:
    def __init__(self, state_space_size, action_space_size):
        self.q_table = np.zeros((state_space_size, action_space_size))
        self.LEARNING_RATE = 0.9
        self.DISCOUNT_FACTOR = 0

    def select_action(self, current_state, action_list, epsilon):
        """

        :param epsilon:
        :param current_state: an integer value that corresponds to a row in the q-table
        :param action_list: a list of integers corresponding to actions that can be performed
        :return: an integer value that corresponds to a column in the current state row
        """
        if np.random.random() > epsilon:
            return self.exploit_strategy(current_state)
        else:
            return explore_strategy(action_list)
        # the last time I did this I used amax instead of argmax

    def exploit_strategy(self, state):
        """

        :return: action index from the q_table
        """
        return np.argmax(self.q_table[state])

    def update_internal_state(self, new_state, state_action_index, reward):
        """
        Update the Q-table here

        :return: nothing
        """

        # Maximum possible Q value in next step (for new state)
        max_future_q = np.max(self.q_table[new_state])

        # Current Q value (for current state and performed action)
        current_q = self.q_table[state_action_index[0], state_action_index[1]]

        # And here's our equation for a new Q value for current state and action
        new_q = (1 - self.LEARNING_RATE) * current_q + self.LEARNING_RATE * (reward[0] + self.DISCOUNT_FACTOR * max_future_q)

        # Update Q table with new Q value
        self.q_table[state_action_index[0], state_action_index[1]] = new_q


class RandomAgent:

    def __init__(self):
        pass


class MonteCarloAgent:

    def __init__(self):
        self.root=Node.Node()

    def get_random_action(self,num_actions):
        random_action=random.randint(0,num_actions-1)
        return random_action

    def expand(self,node,num_actions):

        for i in range(num_actions):
            child=Node.Node(node)
            node.children.append(child)

        random_action = random.randint(0, num_actions - 1)
        return node.children[random_action],random_action

    def reach_leaf(self,exploration_constant):
        node=self.root
        actions=[]

        while(len(node.children)!=0):
            maxsofar=-1
            action=-1
            n=len(node.children)
            for i in range(n):
                child=node.children[i]
                ucb=99999999999
                if(child.visits!=0):
                    ucb=child.score+exploration_constant*np.sqrt(np.log(node.visits)/child.visits)
                if(ucb>maxsofar):
                    maxsofar=ucb
                    action=i
            actions.append(action)
            node=node.children[action]

        return node,actions

    def backprop(self,final_node,reward):

        while(final_node is not None):
            n=final_node.visits
            final_node.visits+=1
            final_node.score=(n*final_node.score+reward)/(n+1)
            final_node=final_node.parent

