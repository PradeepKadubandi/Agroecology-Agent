# Copyright (c) 2019 Elizabeth Ondula, University of Southern California
import itertools
import numpy as np


def get_index(landscape_grid, value):
    for i, x in enumerate(landscape_grid):
        if value in x:
            return i, x.index(value)


def perform_action(landscape, action_tuple):
    """Update cells and plant objects in a landscape.
            Args:
                :param landscape: A 2D array of plant objects.
                :param action_tuple: Integer elements corresponding to action id, position.
                The action i.d is a positive integer value corresponding the decision of an agent.
                We initially choose 2 action i.e 1 and 2. 1 means planting and 2 means harvesting
                A position is the x,y coordinate of a plant i.e the index value of a plant in the landscape list
                [<index>, <action>, <crop>]

            Returns:
                    A 2D array with updated plant objects


            Raises:
                    IOError: An error occurred reading the landscape. 2D Array .

    """
    if action_tuple[1] == 1:
        # if the plant state is 1 then don't plant otherwise plant
        if landscape[action_tuple[0][0]][action_tuple[0][1]].state == 0:
            landscape[action_tuple[0][0]][action_tuple[0][1]].crop_id = action_tuple[2]
            landscape[action_tuple[0][0]][action_tuple[0][1]].state = 1
        else:
            pass  # This can be a penalty given for planting where a crop already exists

    if action_tuple[1] == 2:
        # cell_index = get_index(landscape, action_tuple[1])
        if landscape[action_tuple[0][0]][action_tuple[0][1]].state == 1:
            landscape[action_tuple[0][0]][action_tuple[0][1]].crop_id = 0
            landscape[action_tuple[0][0]][action_tuple[0][1]].state = 0
        else:
            pass  # This can be a penalty given if a harvest is chosen for an empty cell

    updated_landscape = update_landscape(landscape)
    return updated_landscape

def harvestValue(landscape,cell):
    x_coord=cell[0]
    y_coord=cell[1]

    beans=0
    corns=0
    for i in range(-1,2):
        for j in range(-1,2):
            x=x_coord+i
            y=y_coord+j
            if(0<=x<len(landscape) and 0<=y<len(landscape)):
                if(landscape[x][y].crop_id==1):
                    beans+=1
                elif(landscape[x][y].crop_id==2):
                    corns+=1
    if(landscape[x_coord][y_coord].crop_id==1):
        return (15 if corns>=1 else 10)
    elif(landscape[x_coord][y_coord].crop_id==2):
        return 10+beans


def perform_action2(landscape, action_tuple):

    if action_tuple[1] == 1:
        # if the plant state is 1 then don't plant otherwise plant
        if landscape[action_tuple[0][0]][action_tuple[0][1]].state == 0:
            landscape[action_tuple[0][0]][action_tuple[0][1]].crop_id = action_tuple[2]
            landscape[action_tuple[0][0]][action_tuple[0][1]].state = 1
        else:
            pass  # This can be a penalty given for planting where a crop already exists


    if action_tuple[1] == 2:
        # cell_index = get_index(landscape, action_tuple[1])
        currentPlant=landscape[action_tuple[0][0]][action_tuple[0][1]]
        if currentPlant.state == 1:
            if currentPlant.gdd == 5:
                # food value depending on surrounding cells
                currentPlant.foodval=harvestValue(landscape,action_tuple[0])
                currentPlant.crop_id = 0
                currentPlant.state = 0
                currentPlant.gdd = 0
        else:

            currentPlant.foodval-=0

    updated_landscape = update_landscape(landscape)
    return updated_landscape

def update_landscape(landscape):
    """

    :param landscape:
    :return: updated landscape gdd values for crops whose state is 1
    """
    for row in landscape:
        for plant in row:
            if plant.state == 1 and plant.gdd < 5:
                plant.gdd += 1
            else:
                pass
    return landscape


def evaluate_landscape(landscape, size):
    """Scores the a given Landscape.

        A landscape score is an integer value S = sum of cell_scores. Cell_score is defined as a
        an integer value assigned to a cell that has a plant. This value is initially chosen to be 1.
        Note: This is the first proposed evaluation function.

                    Args:
                       :param landscape: A 2D array of plant objects.
                       :param max_plants: A positive integer representing the total number of plants that can be occupied

                   Returns:
                       A tuple where the first index is a positive decimal number and the second index
                       is a positive binary number representing the cell score and a state respectively.
                       The state can be good or bad:

                       (2, 1) or (3, 0)

                   Raises:
                       IOError: An error occurred reading the landscape. 2D Array .

                   """

    # list_of_crops = []
    landscape_score = 0 # This score is currently based on the number of crops in the landscape
    for row in landscape:
        for plant_obj in row:
            if plant_obj.state == 1:
                landscape_score += 1
            else:
                pass

    # print list_of_crops
    # print landscape_score
    if landscape_score > size * size / 2:
        landscape_state = 1  # Good state
    else:
        landscape_state = 0  # Bad state

    return landscape_score, landscape_state

def evaluate_landscape2(landscape, size):
    landscape_score = 0 # This score is currently based on the number of crops in the landscape

    for row in landscape:
        for plant_obj in row:
            landscape_score+=plant_obj.foodval
            plant_obj.foodval=0

    # print list_of_crops
    # print landscape_score
    if landscape_score > size * size / 2:
        landscape_state = 1  # Good state
    else:
        landscape_state = 0  # Bad state

    return landscape_score, landscape_state