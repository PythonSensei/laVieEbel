"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
import sys

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("PythonSensei")
# Then we print our start message to the logs
logging.info("Starting my PythonSensei bot!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end if the turn
    command_queue = []

    dicVal = {}
    for ship in game_map.get_me().all_ships():
        for planet in set(game_map.all_planets()):
            dicVal[planet] = planet.calculate_distance_between(ship) / planet.radius
        planetMax = min(dicVal.items(), key=lambda x: x[1])

#
    command_queue.append(ship.dock(planetMax[0]))
    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
#        command_queue=[]
#        game.send_command_queue(command_queue)
    # TURN END
# GAME END