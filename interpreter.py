# TODO(Robin): Add mapping of action index from agent to simulator to perform action
import itertools
import numpy as np
from environment import Landscape
actions = ['planting', 'harvesting', 'watering']
crops = ['maize', 'beans']
crops_states = range(1, 6)


def generate_action_list(landscape):
    action_list = []
    for index, cell in np.ndenumerate(landscape):
        for action in actions:
            for crop in crops:
                action_vector = [index, action, crop]
                action_list.append(action_vector)

    return action_list


def generate_state_list(landscape):
    state_dict_items = landscape.shape[0] * landscape.shape[1]
    states_list = range(1, state_dict_items + 1)
    landscape_state_def = [states_list, crops, crops_states]
    all_states = list(itertools.product(*landscape_state_def))
    return all_states


my_land = Landscape().default_array



