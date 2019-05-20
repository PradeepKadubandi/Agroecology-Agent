import random
import numpy as np

crops = ['corn', 'bean', 'squash']
actions = ['planting', 'watering', 'harvest']

landscape_rows = 3
landscape_cols = 3
landscape_grid = np.empty([landscape_rows, landscape_cols], dtype=object)
max_reward = 60
reward_list = []
simulation_time = 10


class Plant:
    def __init__(self, crop_id):
        self.crop_id = crop_id

    def display(self):
        return self.crop_id


def simulate(action_list, crop_list):
    # return action to take for a given crop
    crop = random.choice(crop_list)
    action = random.choice(action_list)

    if action == 'planting':
        return plant(Plant(str(crop)))
    elif action == 'watering':
        return water(Plant(str(crop)))
    elif action == 'harvest':
        return harvest()


# Simulator Functions i.e plant, water, harvest.
# Each action results to a score


def plant(plant_obj):
    sample_list = []
    no_of_cells = random.randint(1, ((landscape_rows * landscape_cols) + 1))
    non_empty_cells = []
    for i in range(no_of_cells):
        random_cell_indices = tuple(random.sample(range(landscape_rows), 2))
        sample_list.append(random_cell_indices)
    final_cell_list = list(dict.fromkeys(sample_list))
    for cell in final_cell_list:
        if (landscape_grid[cell[0], cell[1]]) is None:
            landscape_grid[cell[0], cell[1]] = plant_obj
            reward_list.append(1)
        else: 
            non_empty_cells.append(cell)

    # print len(non_empty_cells)
    return ["Planting action performed", landscape_grid]


def water(plant_obj):
    sample_list = []
    no_of_cells = random.randint(1, ((landscape_rows * landscape_cols) + 1))
    for i in range(no_of_cells):
        random_cell_indices = tuple(random.sample(range(landscape_rows), 2))
        sample_list.append(random_cell_indices)
    final_cell_list = list(dict.fromkeys(sample_list))
    for cell in final_cell_list:
        if (landscape_grid[cell[0], cell[1]]) is not None:
            reward_list.append(0.5)
        else:
            reward_list.append(-0.5)
        # elif (landscape_grid[cell[0], cell[1]]).crop_id is None:
        #     reward_list.append(-0.5)

    # print len(non_empty_cells)
    return ["Watering action performed", landscape_grid]


def harvest():
    sample_list = []
    no_of_cells = random.randint(1, ((landscape_rows * landscape_cols) + 1))
    non_empty_cells = []
    for i in range(no_of_cells):
        random_cell_indices = tuple(random.sample(range(landscape_rows), 2))
        sample_list.append(random_cell_indices)
    final_cell_list = list(dict.fromkeys(sample_list))
    for cell in final_cell_list:
        if (landscape_grid[cell[0], cell[1]]) is not None:
            landscape_grid[cell[0], cell[1]] = None
            reward_list.append(1)
        else:
            reward_list.append(-1)
        # else (landscape_grid[cell[0], cell[1]]).crop_id  None:
        #     reward_list.append(-1)
    print len(non_empty_cells)
    return ["Harvesting action performed", landscape_grid]


def get_total_reward(rewards):
    return sum(rewards)


while simulation_time > 0:
    print "***************** Running Simulation at time: ", simulation_time, "*****************"
    print simulate(actions, crops)
    print "***************************End of Simulation, points awarded for action is: ", sum(reward_list)
    simulation_time = simulation_time - 1

