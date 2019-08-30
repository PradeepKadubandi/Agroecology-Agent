import src.environment as env
import unittest

class Landscape_tests(unittest.TestCase):

    def test_total_number_of_states_and_actions(self):
        default_landscape = env.Landscape()
        self._test_total_number_of_states_and_actions(default_landscape, 2 ** 9, 9 * 2 * 1)

        multi_plant_landspace = env.Landscape(crop_list=[1,2])
        self._test_total_number_of_states_and_actions(multi_plant_landspace, 2 ** 9, 9 * 2 * 2)

        # bigger_size_landspace = env.Landscape(size=5)
        # self._test_total_number_of_states_and_actions(bigger_size_landspace, 2 ** 25, 25 * 2 * 2) # 2 ** 25 = 33554432

    def _test_total_number_of_states_and_actions(self, landscape, expected_states, expected_actions):
        total_states = len(landscape.get_all_states())
        total_actions = len(landscape.get_all_actions())
        self.assertEqual(expected_states, total_states)
        self.assertEqual(expected_actions, total_actions)


if __name__ == '__main__':
    unittest.main()
