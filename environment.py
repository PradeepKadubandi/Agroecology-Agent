import numpy as np
import itertools
import functools
import operator


def convert_binary_tuple_to_decimal(tup):
    my_str = " ".join(str(x) for x in tup)
    return int(my_str.replace(" ", ""), 2)


class Plant:

    def __init__(self, crop_id=0):
        self.crop_id = crop_id
        self.gdd = 0
        self.state = 0

    def __repr__(self):
        return str(self.gdd)


class Landscape:
    def __init__(self, location="Los Angeles", size=3, state_list=None, action_list=None, crop_list=None):
        if action_list is None:
            action_list = [1, 2]
        if state_list is None:
            state_list = [0, 1]
        if crop_list is None:
            crop_list = [1]
        self.location = location
        self.size = size
        #self.default = [[Plant()] * self.size for _ in range(self.size)]
        self.default = [[Plant() for j in range(self.size)] for i in range(self.size)]
        self.default_array = np.array(self.default)
        self.all_states = state_list
        self.all_actions = action_list
        self.crop_list = crop_list
        self.cells = size * size
        self.state = 0

    def get_all_states(self):
        """
        Enumerate all possible states of the landscape
        :return: a list of all states
        """
        all_states = [p for p in itertools.product(self.all_states, repeat=self.cells)]
        converted_states = []
        for i in all_states:
            converted_states.append(convert_binary_tuple_to_decimal(i))
        return converted_states

    def get_all_actions(self):
        """
        :return: a list of all actions
        """
        land_arr = self.default_array
        all_actions = []
        for index, cell in np.ndenumerate(land_arr):
            for action in self.all_actions:
                for crop in self.crop_list:
                    action_vector = [index, action, crop]
                    all_actions.append(action_vector)

        return all_actions


