import pytest
from version2 import plant
import numpy as np

class Test_Rewards:
    def test_empty(self):
        e = plant.PlantFactory.getPlantInstance(0)
        assert e.getReward((0, 0), np.zeros((2, 2))) == 0

    def test_bean_surrounded_by_beans(self):
        field = np.ones((2,2), dtype=int) * plant.PlantType.Bean
        e = plant.PlantFactory.getPlantInstance(plant.PlantType.Bean)
        assert e.getReward((0, 0), field) == 10

    def test_bean_surrounded_by_corn(self):
        field = np.ones((3,3), dtype=int) * plant.PlantType.Bean
        field[(0,0)] = plant.PlantType.Corn
        e = plant.PlantFactory.getPlantInstance(plant.PlantType.Bean)
        assert e.getReward((1, 1), field) == 15

    def test_corn_surrounded_by_corn(self):
        field = np.ones((3,3), dtype=int) * plant.PlantType.Corn
        e = plant.PlantFactory.getPlantInstance(plant.PlantType.Corn)
        assert e.getReward((1, 1), field) == 10

    def test_corn_surrounded_by_bean(self):
        field = np.ones((3,3), dtype=int) * plant.PlantType.Corn
        field[(0,0)] = field[(2,2)] = plant.PlantType.Bean
        e = plant.PlantFactory.getPlantInstance(plant.PlantType.Corn)
        assert e.getReward((1, 1), field) == 12