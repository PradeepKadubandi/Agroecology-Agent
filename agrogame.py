import environment as env
import simulator as sim
import agent as agent


class Game:
    def __init__(self, episodes=None, duration=None):
        if episodes is None:
            episodes = 1
        if duration is None:
            duration = 20
        self.duration = duration
        self.episodes = episodes
        self.new_landscape = env.Landscape()
        #self.landscape_default = self.landscape.default
        self.game_over = False

    def start_simulation(self):
        game_episodes = {}
        for i in range(self.episodes):
            print("Starting the Agro-ecosystem simulator")
            game_episodes[i] = self.growing_season_simulation(self.duration)

        print("********************End of game*******************")
        print game_episodes

    def growing_season_simulation(self, duration):
        player = agent.QLearningAgent(len(self.new_landscape.get_all_states()), len(self.new_landscape.get_all_actions()))
        epsilon = 0.2
        evaluation_value = []
        for i in range(duration):
            current_state = self.new_landscape.state
            action_selected = player.select_action(current_state, self.new_landscape.all_actions, epsilon)  # an integer value that will be used to index to all action list
            # print action_selected
            action_tuple = self.new_landscape.get_all_actions()[action_selected]
            #print action_tuple
            new_state = sim.perform_action(self.new_landscape.default, action_tuple)
            #print new_state
            reward = sim.evaluate_landscape(self.new_landscape.default, self.new_landscape.size)
            #print reward
            self.new_landscape.default = new_state
            evaluation_value.append(reward)
            next_state = self.get_state()
            #print next_state, current_state, action_selected, reward
            player.update_internal_state(next_state, [current_state, action_selected], reward)
            print self.new_landscape.default
        return evaluation_value, player.q_table

    def get_state(self):
        landscape_state_list = []
        for row in self.new_landscape.default:
            for plant in row:
                landscape_state_list.append(plant.state)

        landscape_tup = tuple(landscape_state_list)
        return env.convert_binary_tuple_to_decimal(landscape_tup)




