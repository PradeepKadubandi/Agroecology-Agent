import numpy as np
from enum import IntEnum

class PlantType(IntEnum):
    Empty = 0
    Corn = 1
    Bean = 2
    Squash = 3

class Plant:
    '''
    The Plant class (and it's sub classes) are meant to encapsulate the reward design
    for different kinds of plants.
    '''
    def __init__(self, position, field_size):
        self.position = position
        self.field_size = field_size
        self.neighbors = self.getNeighbors()
        self.age = 0
        self.reward = 1.0

    '''
    This is called by environment at each time step. Child plants need to implement
    step method which offers for plant based time step processing.
    '''
    def process_step(self, field, clock):
        self.age += 1
        self._step(field, clock)

    def _step(self, field, clock):
        raise NotImplementedError

    def getNeighbors(self):
        result = []
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if (a, b) != (0, 0):
                    nb = (self.position[0] + a, self.position[1] + b)
                    if 0 <= nb[0] < self.field_size and 0 <= nb[1] < self.field_size:
                        result.append(nb)

        return result

    def isCorner(self):
        if self.position in [(0, 0), (0, self.field_size-1), (self.field_size-1, 0), (self.field_size-1, self.field_size-1)]:
            return True
        return False

class Empty(Plant):
    def __init__(self, position, field_size):
        super().__init__(position, field_size)
        self.reward = 0.0

    def _step(self, field, clock):
        pass

class Bean(Plant):
    def __init__(self, position, field_size):
        super().__init__(position, field_size)

    def _step(self, field, clock):
        if self.age == 1 and any(filter(lambda n: field[n] == PlantType.Corn, self.neighbors)):
            self.reward = 1.1
        if self.reward == 1.1 and 6 <= self.age <= 8 and any(filter(lambda n: self.isCorner(n) and field[n] == PlantType.Squash)):
            self.reward = 1.2

class Corn(Plant):
    def __init__(self, position, field_size):
        super().__init__(position, field_size)

    def _step(self, field, clock):
        if 4 <= clock <= 6 and any(filter(lambda n:field[n] == PlantType.Bean, self.neighbors)):
            self.reward = 1.1
        if clock < 4 and any(filter(lambda n:field[n] == PlantType.Bean, self.neighbors)):
            self.reward = 0.8
        if any(filter(lambda n:field[n] == PlantType.Squash, self.neighbors)):
            self.reward = 0.7

class Squash(Plant):
    def __init__(self, position, field_size):
        super().__init__(position, field_size)
        if (self.isCorner(self.position)):
            self.reward = 1.5
        else:
            self.reward = 0.7

    def _step(self, field, clock):
        pass

class PlantFactory:
    @staticmethod
    def getPlantInstance(position, field):
        plantType = field[position]
        field_size = field.shape[0]
        if plantType == PlantType.Empty:
            return Empty(position, field_size)
        elif plantType == PlantType.Corn:
            return Corn(position, field_size)
        elif plantType == PlantType.Bean:
            return Bean(position, field_size)
        elif plantType == PlantType.Squash:
            return Squash(position, field_size)
        else:
            raise NotImplementedError()