# TODO(Elizabeth):Updating Agent...
import random
import numpy as np


def default_random_select_action(action_list, crop_list):
    selected_action = random.choice(action_list)
    selected_crop = random.choice(crop_list)
    selected_index = random.sample(range(0, 3), 2)
    return [selected_action, selected_crop, selected_index]


class Agent:
    LEARNING_RATE = 0.1
    DISCOUNT = 0.95

    def __init__(self, name, state_space_size, action_space_size):
        self.name = name
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.q_table = np.zeros((self.state_space_size, self.action_space_size))
        # q_table = np.random.uniform(low=-5, high=0, size=(STATE_SPACE_SIZE + [action_size]))

    def q_learning_select_action(self, current_state):
        # select action by looking up the q table
        action = np.argmax(self.q_table[current_state])
        return action

    def update_agent_q_table(self, current_state, reward, next_state, action_taken):
        # Current q value
        current_q = self.q_table[current_state + (action_taken,)]
        # Max possible q value in the next step
        max_q_future = np.argmax(self.q_table[next_state])
        # Update the new q value
        new_q = (1 - self.LEARNING_RATE) * current_q + self.LEARNING_RATE * (reward + self.DISCOUNT * max_q_future)
        self.q_table[current_state + (action_taken,)] = new_q
        return


# for index, cell in np.ndenumerate(q_table):
#     print index, cell

