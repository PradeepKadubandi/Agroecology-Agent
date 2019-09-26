import pytest
from version2 import plant
import numpy as np

@pytest.fixture
def field():
    field_size = 5
    return np.zeros((field_size,field_size))

class Test_Empty:
    def test_default_reward(self, field):
        field_size = field.shape[0]
        test_plant = plant.Empty((0,0), field_size)
        assert test_plant.reward == 0.0

# We can write unit tests similarly for other two plants but
# I am expecting the implementation details will change soon.
# So for now, only adding this to make sure the code runs as expected.
class Test_Corn:
    def test_default_reward(self, field):
        field_size = field.shape[0]
        test_plant = plant.Corn((0,0), field_size)
        assert test_plant.reward == 1.0

    def test_reward_boost_from_bean(self, field):
        field_size = field.shape[0]
        test_plant = plant.Corn((1,1), field_size)
        field[(1,1)] = plant.PlantType.Corn
        field[(1,0)] = plant.PlantType.Bean
        test_plant.process_step(field, 5)
        assert test_plant.reward == 1.1

    def test_reward_drop_from_bean_early_planting(self, field):
        field_size = field.shape[0]
        test_plant = plant.Corn((1,1), field_size)
        field[(1,1)] = plant.PlantType.Corn
        field[(1,0)] = plant.PlantType.Bean
        test_plant.process_step(field, 3)
        assert test_plant.reward == 0.8

    def test_reward_drop_from_squash(self, field):
        field_size = field.shape[0]
        test_plant = plant.Corn((1,1), field_size)
        field[(1,1)] = plant.PlantType.Corn
        field[(1,0)] = plant.PlantType.Bean
        field[(0,1)] = plant.PlantType.Squash
        test_plant.process_step(field, 5)
        assert test_plant.reward == 0.7