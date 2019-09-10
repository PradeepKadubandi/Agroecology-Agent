# Copyright (c) 2019 Elizabeth Ondula, University of Southern California
import agrogame as game
import cProfile
# Start the game

new_game = game.Game(100000,36,"monte-carlo",6)

# print (new_game.landscape.all_actions)
# print (new_game.landscape.all_states)
cProfile.run('new_game.start_simulation()')


