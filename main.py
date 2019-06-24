import simulator as sim
import agent as agent
import numpy as np
import environment as env

# Initialize the landscape area
MY_LAND = env.Landscape().default_array

state_space = env.state_spaces(MY_LAND)
action_space = env.action_space(MY_LAND)
my_agent = agent.Agent("leez", len(state_space), len(action_space))
q_table = my_agent.q_table

print state_space
# print "************************************************************************************"
# print "************************************************************************************"
# print "************************************************************************************"
# print "____________________________________________________________________________________"
# print "************************************ STATE AT TIME EQUAL 0 **************************************"
# for index, cell in np.ndenumerate(MY_LAND):
#     print index, cell
#
#
# action_result = sim.perform_action(MY_LAND, [ "planting", "maize", [0, 0]])
# MY_LAND = action_result[1]
# print "************************************************************************************"
# print "************************************************************************************"
# print "************************************************************************************"
# print "____________________________________________________________________________________"
# print "************************************ STATE AFTER PLANTING ACTION HAS BEEN TAKEN AT TIME EQUAL 1 **************************************"
#
# for i, c in np.ndenumerate(MY_LAND):
#     print i, c


# Initialize no. of runs
#RUNS = 10

# Let's start the Game

# while RUNS:
#     current_state = MY_LAND
#     action_list = agent.default_random_select_action()
#     action_result = sim.perform_action(MY_LAND, action_list)
#     # update agent on reward and new state
#     MY_LAND = action_result[1]
#     reward = action_result[0]
#     next_land_state = sim.update_landscape(MY_LAND)
#     #agent.update_agent_q_table(current_state, reward, next_land_state, action_list[0])
#     print reward, next_land_state
#     RUNS -= 1
#
