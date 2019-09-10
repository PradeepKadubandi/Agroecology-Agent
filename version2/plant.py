import numpy as np
from enum import IntEnum

class PlantType(IntEnum):
    Empty = 0
    Bean = 1
    Corn = 2

class Plant:
    '''
    The Plant class (and it's sub classes) are meant to encapsulate the reward design
    for different kinds of plants. So this class doesn't concern itself with the actual
    layout of field or it's own position. However each different plant class will implement
    (their) specific rewards given the field layout and it's own position in the field.
    '''
    def __init__(self, plantType):
        self.plantType = plantType

    def getReward(self, position, field):
        raise NotImplementedError()

    def getNeighbors(self, position, field):
        assert field.ndim == 2 and field.shape[0] == field.shape[1]

        field_size = field.shape[0]
        result = []
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if (a, b) != (0, 0):
                    nb = (position[0] + a, position[1] + b)
                    if 0 <= nb[0] < field_size and 0 <= nb[1] < field_size:
                        result.append(nb)

        return result

class Empty(Plant):
    def __init__(self):
        super().__init__(PlantType.Empty)

    def getReward(self, position, field):
        return 0

class Bean(Plant):
    def __init__(self):
        super().__init__(PlantType.Bean)

    def getReward(self, position, field):
        neighbors = self.getNeighbors(position, field)
        for neighbor in neighbors:
            if field[neighbor] == PlantType.Corn:
                return 15

        return 10

class Corn(Plant):
    def __init__(self):
        super().__init__(PlantType.Corn)

    def getReward(self, position, field):
        reward = 10
        neighbors = self.getNeighbors(position, field)
        for neighbor in neighbors:
            if field[neighbor] == PlantType.Bean:
                reward += 1

        return reward

class PlantFactory:
    '''
    Since plant classes only encapsulate the reward design, they are
    essentially one instance per plant type (for the entire program).
    So we maintain a factory of plant types that can give the right instance
    of plant class given an integer value (plant type). 
    '''
    plantTypeToPlantInstance = {0: Empty(), 1: Bean(), 2:Corn()}
    
    @staticmethod
    def getPlantInstance(plantType):
        if plantType not in PlantFactory.plantTypeToPlantInstance:
            raise NotImplementedError() #This should be something like UnrecognizedType or KeyNotFound
        return PlantFactory.plantTypeToPlantInstance[plantType]