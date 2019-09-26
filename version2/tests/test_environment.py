import pytest
from version2.environment import NaturalSequenceEnvironment
import numpy as np

class Test_NaturalSequenceEnvironment:
    def test_steps_shorter_harvest_period(self):
        test_env = NaturalSequenceEnvironment(harvest_period=2, field_size=3, no_of_crops=2)
        field, reward, done, info = test_env.step(0) # 0 action is plant type 1 i.e., Corn
        assert reward == 0.0
        assert done == False
        assert field[(0, 0)] == 1
        field, reward, done, info = test_env.step(1) # 1 action is plant type 2 i.e., Bean
        assert reward != 0.0
        assert done == True
        assert field[(0, 0)] == 1
        assert field[(0, 1)] == 2

    def test_steps_larger_harvest_period(self):
        test_env = NaturalSequenceEnvironment(harvest_period=5, field_size=2, no_of_crops=2)
        for i in range(4):
            field, reward, done, info = test_env.step(0)
            assert done == False
            assert reward == 0.0
            assert np.count_nonzero(field) == i+1

        field, reward, done, info = test_env.step(0)
        assert done == True
        assert reward != 0.0
        assert np.count_nonzero(field) == 4

