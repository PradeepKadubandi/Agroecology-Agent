import numpy as np
import itertools

ACTIONS = ['planting', 'harvesting', 'watering']
CROPS = ['maize', 'beans']
CROP_STATES = range(1, 6)


class Plant:
    def __init__(self, crop_id="None", stage=0, water=0):
        self.crop_id = crop_id
        Plant.stage = stage
        Plant.water = water

    def __repr__(self):
        return self.crop_id


class Landscape:

    def __init__(self, location="Los Angeles", size=3):
        self.location = location
        self.size = size
        self.default = [[Plant()] * self.size for _ in range(self.size)]
        self.default_array = np.array(self.default)

    def ask_size(self):
        while True:
            try:
                grid_size = int(input("input grid length and width\n"))
                if grid_size < 2:
                    print ("invalid int")
                else:
                    self.size = grid_size
            except ValueError:
                print ("invalid input")

    def make_landscape(self):
        return [[Plant()] * self.size for _ in range(self.size)]


def state_spaces(landscape_instance):
    landscape_arr = np.array(landscape_instance)
    state_dict_items = landscape_arr.shape[0] * landscape_arr.shape[1]
    states_list = range(1, state_dict_items + 1)
    landscape_state_def = [states_list, CROPS, CROP_STATES]
    all_states = list(itertools.product(*landscape_state_def))
    chunks = [all_states[x:x + 10] for x in xrange(0, len(all_states), 10)]
    new_state_changed = map(list, zip(*chunks))
    return new_state_changed


def action_space(landscape_instance):
    land_arr = np.array(landscape_instance)
    action_list = []
    for index, cell in np.ndenumerate(land_arr):
        for action in ACTIONS:
            for crop in CROPS:
                action_vector = [index, action, crop]
                action_list.append(action_vector)

    return action_list
