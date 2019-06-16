import numpy as np
import environment as env


def print_land(grid):
    for row in grid:
        print(row)


def get_soil_moisture(grid_cell):
    return "10"


def perform_action(grid, action):
    # action (name, crop, position) e.g ['planting', 'maize', (0,0)]
    if action[0] == 'planting':
        if (grid[action[2][0], action[2][1]]) == "None":
            grid[action[2][0], action[2][1]] == env.Plant(str(action[1]))
            reward = 10
            return reward
        else:
            reward = -1
            return reward
    elif action[0] == 'harvesting':
        if (grid[action[2][0], action[2][1]]) == "None":
            reward = -1
            return reward
        else:
            grid[action[2][0], action[2][1]] == env.Plant("None")
            reward = 10
            return reward

    elif action[0] == 'watering':
        if get_soil_moisture(grid[action[2][0], action[2][1]]) < 10:
            reward = 15
            return reward
        else:
            reward = -2
            return reward


my_land = env.Landscape().default_array
print my_land
