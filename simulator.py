import random
import numpy as np
import environment as env


def perform_action(land, action):
    """Implements an action to a landscape.

        An action is chosen by different types of agents to be performed on the land.

        Args:
            land: A 2D array with objects
            action: A list with items as followsa

        Returns:
           A list with reward (int), new_land(2D array)
           """
    if action[1] == 'planting':
        if (land[action[0][0], action[0][1]]).crop_id == "None":
            (land[action[0][0], action[0][1]]) = env.Plant(str(action[2]))
            return [1, land]
        return [-1, land]
    elif action[0] == 'harvesting':
        if (land[action[0][0], action[0][1]]).crop_id == "None":
            return [-1, land]
        return [10, land] if (land[action[0][0], action[0][1]]).stage == 5 else [-1, land]

    elif action[0] == 'watering':
        ideal_water = range(4, 10)
        if (land[action[0][0], action[0][1]]).crop_id == "None":
            return [-1, land]
        return [1, land] if (land[action[0][0], action[0][1]]).water in ideal_water else [-1, land]


def update_landscape(arr):
    # update landscape status i.e crops status
    for ix, iy in np.ndindex(arr.shape):
        if arr[ix, iy].crop_id == "None":
            pass
        if arr[ix, iy].crop_id == "maize":
            arr[ix, iy].stage = random.randint(0, 5)
            arr[ix, iy].water = random.randint(0, 9)

        if arr[ix, iy].crop_id == "bean":
            arr[ix, iy].stage = random.randint(0, 9)
            arr[ix, iy].water = random.randint(0, 9)

    return arr


