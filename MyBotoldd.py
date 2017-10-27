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

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Dakynee")
# Then we print our start message to the logs
logging.info("Starting my newbie bot!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        # For each planet in the game (only non-destroyed planets are included)
        # Bugged part
        dicVal={}
        newdic={}
        for planet in game_map.all_planets():
            dicVal[planet] = planet.calculate_distance_between(ship)
        newdic = sorted(dicVal.items(), key=lambda x: x[1])
        # for nudes in dickpick
        for planet in newdic:
            if planet[0].is_full():
                if planet[0].owner.id == game_map.my_id:
                    continue
                else:
                    command_queue.append(ship.navigate(planet[0],game_map,speed=int(hlt.constants.MAX_SPEED),ignore_ships=True,ignore_planets=True))
            # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
            elif ship.can_dock(planet[0]):
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(planet[0]))
            else:

                navigate_command = ship.navigate(
                    ship.closest_point_to(planet[0]),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)
            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
