import random
import numpy as np
import simulator as sim

state_size = 99
action_size = 22
LEARNING_RATE = 0.1
# Measure of how much we value future reward vs current reward
DISCOUNT = 0.95
EPISODES = 10000

size_of_observation = 3

STATE_SPACE_SIZE = [9] * size_of_observation

q_table = np.random.uniform(low=-5, high=0, size=(STATE_SPACE_SIZE + [action_size]))


def default_random_select_action():
    # type: () -> object
    action_list = ['planting', 'harvesting', 'watering']
    crop_list = ['maize', 'bean']
    selected_action = random.choice(action_list)
    selected_crop = random.choice(crop_list)
    selected_index = random.sample(range(0, 3), 2)
    return [selected_action, selected_crop, selected_index]


# Q-LEARNING IMPLEMENTATION

def q_learning_select_action(current_state, time_step):
    # select action by looking up the q table
    action = np.max(q_table[current_state])

    # get reward from taking the action
    reward = sim.perform_action(current_state, action)

    # Max possible q value in the next step
    max_q_future = np.max(q_table[sim.get_next_state(time_step)])

    # Current Q value
    current_q = q_table[current_state + (action, )]

    # Update the new q value
    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_q_future)
    q_table[current_state + (action, )] = new_q

    return action
