import simulator as sim
import environment as env
import random
import numpy as np

state_size = 99
action_size = 22

# initialize Q table to 0
q_table = np.zeros((state_size, action_size))

my_land = env.Landscape().default_array


def default_random_select_action():
    action_list = ['planting', 'harvesting', 'watering']
    crop_list = ['maize', 'bean']
    selected_action = random.choice(action_list)
    selected_crop = random.choice(crop_list)
    selected_index = random.sample(range(0, 2), 2)

    return sim.perform_action(my_land, [selected_action, selected_crop, selected_index])


def q_learning_select_action():
    """
    Q-learning training
    :return: Action from q learning
    """
    return "TODO"


print default_random_select_action()
