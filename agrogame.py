import environment as env
import simulator as sim
import agent as agent


class Game:
    def __init__(self, episodes=None, duration=None, type="q-learning"):

        if episodes is None:
            episodes = 10
        if duration is None:
            duration = 20

        self.type = type
        self.duration = duration
        self.episodes = episodes

        # self.landscape_default = self.landscape.default
        self.game_over = False

    def start_simulation(self):
        game_episodes = {}

        total=0

        print("Starting the Agro-ecosystem simulator")

        if(self.type=="q-learning"):
            for i in range(self.episodes):
                game_episodes[i] = self.growing_season_simulation(self.duration)

        elif(self.type=="monte-carlo"):
            player=agent.MonteCarloAgent()

            for i in range(self.episodes):

                game_episodes[i]=self.monte_carlo_simulation(player)
                total+=game_episodes[i]
                print(total/(i+1))

        print("********************End of game*******************")
        print (game_episodes)

    def monte_carlo_simulation(self,player):
        self.new_landscape = env.Landscape()

        last_node,actions=player.reach_leaf(0.50) #returns last node and all the actions performed
        duration_counter=0

        num_possible_actions=len(self.new_landscape.get_all_actions())

        for action in actions:
            action_tuple = self.new_landscape.get_all_actions()[action]
            new_state = sim.perform_action(self.new_landscape.default, action_tuple)
            self.new_landscape.default = new_state
            duration_counter += 1

        if(duration_counter<self.duration):
            #expand
            last_node,action_expanded=player.expand(last_node,num_possible_actions) #returns the final node get reward and action which rollout is chosen
            action_tuple = self.new_landscape.get_all_actions()[action_expanded]
            new_state = sim.perform_action(self.new_landscape.default, action_tuple)
            self.new_landscape.default = new_state
            duration_counter += 1

        for i in range(self.duration-duration_counter):
            random_action=player.get_random_action(num_possible_actions)
            action_tuple = self.new_landscape.get_all_actions()[random_action]
            new_state = sim.perform_action(self.new_landscape.default, action_tuple)
            self.new_landscape.default = new_state

        reward = sim.evaluate_landscape(self.new_landscape.default, self.new_landscape.size)[0]
        player.backprop(last_node,reward)
        return reward







    def growing_season_simulation(self, duration):
        player = agent.QLearningAgent(len(self.new_landscape.get_all_states()),
                                      len(self.new_landscape.get_all_actions()))
        evaluation_value = []
        epsilon = 0.2
        for i in range(duration):
            current_state = self.new_landscape.state
            action_selected = player.select_action(current_state, self.new_landscape.all_actions,
                                                   epsilon)  # an integer value that will be used to index to all
            # action list
            # print action_selected
            action_tuple = self.new_landscape.get_all_actions()[action_selected]
            # print action_tuple
            new_state = sim.perform_action(self.new_landscape.default, action_tuple)
            # print new_state
            reward = sim.evaluate_landscape(self.new_landscape.default, self.new_landscape.size)
            # print reward
            self.new_landscape.default = new_state
            evaluation_value.append(reward)
            next_state = self.get_state()
            # print next_state, current_state, action_selected, reward
            player.update_internal_state(next_state, [current_state, action_selected], reward)
            print (self.new_landscape.default)
        return evaluation_value, player.q_table

    def get_state(self):
        landscape_state_list = []
        for row in self.new_landscape.default:
            for plant in row:
                landscape_state_list.append(plant.state)

        landscape_tup = tuple(landscape_state_list)
        return env.convert_binary_tuple_to_decimal(landscape_tup)
