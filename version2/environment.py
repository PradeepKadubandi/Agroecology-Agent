from gym.spaces import Discrete
from gym.spaces import Box
from gym import Env
import numpy as np
import plant

class EnvironmentV2(Env):
    '''
    This envoronment implements the required open ai gym based environment interface
    so that we can run their implementations against our environment.
    For now, this uses the approach of planting all crops on day1 and harvesting once
    the field is completely planed (i.e., notion of time is not implemented). We will
    obviously need to adapt this implementation to eventually support notion of time.
    Also, in future what we really should do is call the C++ code for implementation
    of this class - when we do that, this class will act as an adapter of our real
    environment implementation (in C++) to open AI gym interface.
    '''
    Default_Start_Index = (0, 0)

    def __init__(self, field_size=5, no_of_crops=2):
        self.field_size = field_size
        self.no_of_crops = no_of_crops
        self.current_index = EnvironmentV2.Default_Start_Index
        self.field = np.zeros((field_size, field_size))
        self.action_space = Discrete(no_of_crops)
        self.observation_space = Box(low=0, high=no_of_crops-1, shape=(field_size, field_size), dtype=int)
    
    def reset(self):
        self.current_index = EnvironmentV2.Default_Start_Index
        self.field[:] = 0.0
        return self.field

    def step(self, action):
        self.field[self.current_index] = action # Todo: Do we need to make a new copy?
        done = self.current_index == (self.field_size-1, self.field_size-1)
        reward = 0.0
        info = None
        if not done:
            self.current_index = np.unravel_index(1 + np.ravel_multi_index(self.current_index, self.field.shape), self.field.shape)
        else:
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
        for x in range(self.field_size):
            for y in range(self.field_size):
                plantInstance = plant.PlantFactory.getPlantInstance(self.field[(x, y)])
                total += plantInstance.getReward((x, y), self.field)

        return total
