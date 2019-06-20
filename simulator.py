import random
import numpy as np
import environment as env
import agent as agent


def perform_action(land, action):
    """Implements an action to a landscape.

        An action is chosen by different types of agents to be performed on the land.

        Args:
            land: A 2D array with objects
            action: A list with items as follows [ action_name, crop_name, index]

        Returns:
           A list with reward (int), new_land(2D array)
           """
    if action[0] == 'planting':
        if (land[action[2][0], action[2][1]]).crop_id == "None":
            (land[action[2][0], action[2][1]]) = env.Plant(str(action[1]))
            return [1, land]
        return [-1, land]
    elif action[0] == 'harvesting':
        if (land[action[2][0], action[2][1]]).crop_id == "None":
            return [-1, land]
        return [10, land] if (land[action[2][0], action[2][1]]).stage == 5 else [-1, land]

    elif action[0] == 'watering':
        ideal_water = range(4, 10)
        if (land[action[2][0], action[2][1]]).crop_id == "None":
            return [-1, land]
        return [1, land] if (land[action[2][0], action[2][1]]).water in ideal_water else [-1, land]


# Initialize the landscape area
MY_LAND = env.Landscape().default_array

# Start Simulation
for i in range(100):
    # Agent or human selects an action to perform
    selected_actions = agent.default_random_select_action()
    action_result = perform_action(MY_LAND, selected_actions)
    arr = action_result[1]
    reward = action_result[0]

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

    print arr
    print "Action selected: ", selected_actions[0], " Crop chosen: ", selected_actions[1], \
        " Location", selected_actions[2], "Reward Received: ", reward


def get_current_state():
    """
     Returns: The current landscape state at the current simulation time
    """
    current_land_state = MY_LAND
    return current_land_state
