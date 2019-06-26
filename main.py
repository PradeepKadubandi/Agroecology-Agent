import random
import simulator as sim
import agent as agent
import numpy as np
import environment as env

# Initialize the landscape area
MY_LAND = env.Landscape().default_array
DAYS = 100
EPISODES = 1000

state_space = env.state_spaces(MY_LAND)
action_space = env.action_space(MY_LAND)
my_agent = agent.Agent("leez", len(state_space), len(action_space))

# Initialize no. of runs

my_file = open("actions.txt", "w")

while DAYS:
    current_state = sim.get_next_state(state_space)
    # # action_list = agent.default_random_select_action(env.ACTIONS, env.CROPS)
    action_list = my_agent.q_learning_select_action([current_state])
    action_result = sim.perform_action(np.array(MY_LAND), action_space[action_list[1]])
    # update agent on reward and new state
    MY_LAND = action_result[1]
    reward = action_result[0]
    next_land_state = sim.get_next_state(state_space)
    my_agent.update_agent_q_table(current_state, reward, next_land_state, action_list[1])
    my_file.write(str(action_space[action_list[1]]) + '\n')
    DAYS -= 1


