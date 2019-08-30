import src.simulator as sim
import src.environment as env
import unittest

class simulator_tests(unittest.TestCase):

    def test_perform_action_planting(self):
        pass
        l = env.Landscape().default
        index = (0, 0)
        self.assertEquals(0, l[index].state)

        s = sim.perform_action(l, [index, 1, 1])
        self.assertEquals(1, l[index].state)

if __name__ == '__main__':
    unittest.main()