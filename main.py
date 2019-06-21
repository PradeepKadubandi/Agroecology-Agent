import simulator as sim
import agent as agent
import environment as env

# Initialize the landscape area
MY_LAND = env.Landscape().default_array
# Initialize no. of runs
RUNS = 100

# Let's start the Game

while RUNS:
    current_state = MY_LAND
    action_list = agent.default_random_select_action()
    action_result = sim.perform_action(MY_LAND, action_list)
    # update agent on reward and new state
    MY_LAND = action_result[1]
    reward = action_result[0]
    next_land_state = sim.update_landscape(MY_LAND)
    agent.update_agent_q_table(current_state, reward, next_land_state, action_list[0])
    print next_land_state
    RUNS -= 1

