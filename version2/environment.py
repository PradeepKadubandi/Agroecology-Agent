from gym.spaces import Discrete
from gym.spaces import Box
from gym import Env
import numpy as np
from version2 import plant

class Environment(Env):
    '''
    This envoronment implements the required open ai gym based environment interface
    so that we can run their implementations against our environment.
    In future what we really should do is call the C++ code for implementation
    of this class - when we do that, this class will act as an adapter of our real
    environment implementation (in C++) to open AI gym interface.
    '''

    def __init__(self, harvest_period=30, field_size=5, no_of_crops=2):
        self.harvest_period = harvest_period
        self.field_size = field_size
        self.no_of_crops = no_of_crops

        self.field = np.zeros((field_size, field_size))
        self.common_empty_instance = plant.Empty((0, 0), field_size) #Optimization, Empty plant is special because 'position' is irrelavant, so we can have one instance for all cells
        self.plants = np.full_like(self.field, self.common_empty_instance, dtype=plant.Plant)
        self.clock = 0

        self.action_space = Box(low=0, high=no_of_crops, shape=(field_size, field_size), dtype=int)
        self.observation_space = Box(low=0, high=no_of_crops, shape=(field_size, field_size), dtype=int)
    
    def reset(self):
        self.field[:] = 0.0
        self.plants[:] = self.common_empty_instance
        self.clock = 0
        return self.field

    def step(self, action):
        self.clock += 1
        if any(self.field[self.field != action]):
            raise ValueError('Plants that are already in field cannot be removed')

        # TODO: There may be faster way to do the below than enumerating? Using numpy mask arrays?
        for index in np.ndindex(self.field.shape):
            if self.field[index] == 0 and action[index] != 0:
                self.field[index] = action[index]
                self.plants[index] = plant.PlantFactory.getPlantInstance(index, self.field)
            self.plants[index].process_step(self.field, self.clock)

        done = (self.clock == self.harvest_period)
        reward = 0.0
        info = None
        # if not done:
        #     self.current_index = np.unravel_index(1 + np.ravel_multi_index(self.current_index, self.field.shape), self.field.shape)
        if done:
            reward = self.__get_reward()
        return self.field, reward, done, info

    def close(self):
        pass

    def render(self, mode):
        print (self.field)

    def seed(self, seed=None):
        return [] # Todo: Should we need to pass a seed?

    def __get_reward(self):
        total = 0.0
        # for x in range(self.field_size):
        #     for y in range(self.field_size):
        #         plantInstance = plant.PlantFactory.getPlantInstance(self.field[(x, y)])
        #         total += plantInstance.getReward((x, y), self.field)
        # Again, there may be faster way to do this?
        for index in np.ndindex(self.plants.shape):
            total += self.plants[index].reward
        return total

class NaturalSequenceEnvironment(Environment):
    '''
    This environment restricts the action space to C where C = number of crops.
    At each time step, this chooses next cell automatically as the place to
    plant the crop (next cell being the next index in array). So, in each
    time step, this environment only plants one cell.
    '''

    def __init__(self, harvest_period=30, field_size=5, no_of_crops=2):
        super().__init__(harvest_period, field_size, no_of_crops)
        self.action_space = Discrete(no_of_crops)
        self.current_index = 0

    def step(self, action):
        # Hack for adjusting the action value from Discrete action space which runs from 0 to n-1 to
        # our plant enumeration which runs from 1 to n
        action += 1
        super_action = np.array(self.field)
        if self.current_index < self.field_size * self.field_size:
            super_action.flat[self.current_index] = action
            self.current_index += 1
        return super().step(super_action)

