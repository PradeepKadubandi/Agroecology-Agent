import simulator as sim
import environment as env
import random
import numpy as np

state_size = 99
action_size = 22
LEARNING_RATE = 0.1
# Measure of how much we value future reward vs current reward
DISCOUNT = 0.95
EPISODES = 10000

size_of_observation = 3

STATE_SPACE_SIZE = [9] * size_of_observation

q_table = np.random.uniform(low=-10, high=0, size=(STATE_SPACE_SIZE + [action_size]))


def default_random_select_action():
    action_list = ['planting', 'harvesting', 'watering']
    crop_list = ['maize', 'bean']
    selected_action = random.choice(action_list)
    selected_crop = random.choice(crop_list)
    selected_index = random.sample(range(0, 2), 2)

    return sim.perform_action(my_land, [selected_action, selected_crop, selected_index])


# Q-LEARNING IMPLEMENTATION

for episode in range(EPISODES):
    my_land = env.Landscape().default_array
    # True means the simulation is done or terminated
    done = False

    while not done:
        # select action from Q table
        # TODO
        index = random.sample(range(0, 2), 2)
        action = q_table[index]
        # Or select random action
        new_land_state, reward, done = sim.perform_action(my_land, action)

        # Update Q table if simulation did not end

        # new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        # Otherwise if goal is achieved when simulation has ended, update Q table with the reward directly
