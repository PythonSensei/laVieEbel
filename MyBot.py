#1.1. Si le vaisseau n'est pas en vol
#1.1.1. Vaisseau suivant
#1.2. Sinon
#1.2. Pour chaque planète (de la plus proche à la plus lointaine)
#1.2.1. Si la planète est à moi
#1.2.1.1. Si pas plein
#1.2.1.1.1. Si peut dock
#1.2.1.1.1.1. Dock
#1.2.1.1.2. Si loin
#1.2.1.1.2.1. Aller à la planète
#1.2.1.2. Si plein
#1.2.1.2.1. Planète suivante
#1.2.2. Sinon si la planète est à l'ennemi
#1.2.2.1. Aller à coté des vaisseaux dockés (sans suicide)
#1.2.3. Sinon (la planète n'est à personne)
#1.2.3.1. Si peut dock
#1.2.3.1.1. Aller se docker
#1.2.3.2. Sinon
#1.2.3.2.1. Se rapprocher puis docker
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Dakyne")
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
        #1.1. Si le vaisseau n'est pas en vol#
        logging.debug("———")
        logging.debug("Current ship : %s" % ship.id)
        #If the ship is docked#
        logging.debug("Docking status ship : %s" % ship.docking_status)
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            #1.1.1. Vaisseau suivant#
            logging.debug("Ship %s is not flying" % ship.id)
            continue

        #1.2. Sinon#
        else:
        #1.2. Pour chaque planète (de la plus proche à la plus lointaine)#
            logging.debug("else")
            dictVal={}
            for planet in game_map.all_planets():
                dictVal[planet] = planet.calculate_distance_between(ship)
            listVal = sorted(dictVal.items(), key=lambda x: x[1])

            logging.debug("For each planet")
            for planet in listVal:
        #1.2.1. Si la planète est à moi#
                if planet[0].owner == game_map.get_me():
        #1.2.1.1. Si pas plein#
                    if not planet[0].is_full():
        #1.2.1.1.1. Si peut dock#
                        if ship.can_dock(planet[0]):
        #1.2.1.1.1.1. Dock#
                            logging.debug("Planet %s is empty" % planet[0].id)
                            command_queue.append(ship.dock(planet[0]))
                            logging.debug("Ship %s can dock on this planet" % ship.id)
        #1.2.1.1.2. Si loin#
                        else:
        #1.2.1.1.2.1. Aller à la planète#
                            logging.debug("Move to my planet %s" % planet[0].id)
                            navigate_command = ship.navigate(ship.closest_point_to(planet[0]),game_map,speed=int(hlt.constants.MAX_SPEED),ignore_ships=False)
                        break
        #1.2.1.2. Si plein#
                    else:
        #1.2.1.2.1. Planète suivante#
                        continue
        #1.2.2. Sinon si la planète est à l'ennemi#
                elif not planet[0].owner == game_map.get_me() and not planet[0].owner == None:
                    logging.debug("Test")
        #1.2.2.1. Aller à coté des vaisseaux dockés (sans suicide)#
                    dictShip={}
                    for vaisseaux in planet[0].all_docked_ships():
                        dictShip[vaisseaux] = vaisseaux.calculate_distance_between(ship)
                    listShip = sorted(dictShip.items(), key=lambda x: x[1])
                    #for vaiss in listShip:
                    #    if not vaiss[0].owner == game_map.get_me():# À priori ce test ne sert à rien
                    navigate_command = ship.navigate(ship.closest_point_to(vaiss[0]),game_map,speed=int(hlt.constants.MAX_SPEED),ignore_planets=False)
                    logging.debug("Move to ship %s" % vaiss[0].id)
                    #        break
                    break

        #1.2.3. Sinon (la planète n'est à personne)#
                else:
        #1.2.3.1. Si peut dock#
                    if ship.can_dock(planet[0]):
        #1.2.3.1.1. Aller se docker#
                        command_queue.append(ship.dock(planet[0]))
                        logging.debug("Ship %s can dock on this empty planet" % ship.id)
        #1.2.3.2. Sinon#
                    else:
        #1.2.3.2.1. Se rapprocher puis docker#
                        logging.debug("Moving to empty planet %s" % planet[0].id)
                        navigate_command = ship.navigate(ship.closest_point_to(planet[0]),game_map,speed=int(hlt.constants.MAX_SPEED),ignore_ships=False)
                    break
                break

        if navigate_command:
            command_queue.append(navigate_command)
                


    # Send our set of commands to the Halite engine for this turn
    logging.debug("     ")
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
