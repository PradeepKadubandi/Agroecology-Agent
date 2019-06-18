import numpy as np
import random
import environment as env


def print_land(grid):
    for row in grid:
        print(row)


def get_soil_moisture(grid_cell):
    return "10"


def perform_action(land, action):
    # action (name, crop, position) e.g ['planting', 'maize', (0,0)]
    if action[0] == 'planting':
        if (land[action[2][0], action[2][1]]).crop_id == "None":
            (land[action[2][0], action[2][1]]) = env.Plant(str(action[1]))
            r = 1
            return r, land
        else:
            r = -1

            return r, land
    elif action[0] == 'harvesting':
        if (land[action[2][0], action[2][1]]).crop_id == "None":
            r = -1
            return r, land
        else:
            (land[action[2][0], action[2][1]]).crop_id = env.Plant("None")
            r = 10
            return r, land

    elif action[0] == 'watering':
        if get_soil_moisture(land[action[2][0], action[2][1]]) < 10:
            r = 15
            return r, land
        else:
            r = -2
            return r, land


my_land = env.Landscape().default_array

for i in range(5):
    action_list = ['planting', 'harvesting', 'watering']
    crop_list = ['maize', 'bean']
    selected_action = random.choice(action_list)
    selected_crop = random.choice(crop_list)
    selected_index = random.sample(range(0, 2), 2)
    reward, grid = perform_action(my_land, [selected_action, selected_crop, selected_index])
    print selected_action
    print reward, grid


