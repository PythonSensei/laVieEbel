"""
Refaire l'ordre des actions :
1.1. Si le vaisseau n'est pas en vol"""
logging.debug("———")
logging.debug("Traitement du vaisseau %s" % ship.id)
"""If the ship is docked"""
if ship.docking_status != ship.DockingStatus.UNDOCKED:
    """1.1.1. Vaisseau suivant"""
    logging.debug("Le vaisseau %s n'est pas en vol" % ship.id)
    continue

"""1.2. Sinon"""
else:
"""1.2. Pour chaque planète (de la plus proche à la plus lointaine)"""
    dictVal={}
    for planet in game_map.all_planets():
        dictVal[planet] = planet.calculate_distance_between(ship)
    listVal = sorted(dictVal.items(), key=lambda x: x[1])
    
    logging.debug("Pour chaque planète")
    for planet in listVal:
"""1.2.1. Si la planète est à moi"""
        if planet[0].owner == game_map.get_me():
"""1.2.1.1. Si pas plein"""
            if not planet[0].is_full():
"""1.2.1.1.1. Si peut dock"""
                if ship.can_dock(planet[0]):
"""1.2.1.1.1.1. Dock"""
                    logging.debug("La planète %s est vide" % planet[0].id)
                    command_queue.append(ship.dock(planet[0]))
                    logging.debug("Le ship %s peut dock sur la planète précédente" % ship.id)
                    break
"""1.2.1.1.2. Si loin"""
                else:
"""1.2.1.1.2.1. Aller à la planète"""
                    logging.debug("Déplacement vers la planète %s" % planet[0].id)
                    command_queue.append(ship.navigate(ship.closest_point_to(planet[0]),game_map,speed=int(hlt.constants.MAX_SPEED),ignore_ships=False))
                    break
"""1.2.1.2. Si plein"""
            else:
"""1.2.1.2.1. Planète suivante"""
                continue
"""1.2.2. Sinon si la planète est à l'ennemi"""
        elif not (planet[0].owner == game_map.get_me() and planet[0].owner == None):
"""1.2.2.1. Aller à coté des vaisseaux dockés (sans suicide)"""
            for vaisseaux in planet[0].all_docked_ships():
                dictShip[vaisseaux] = vaisseaux.calculate_distance_between(ship)
            listShip = sorted(dictShip.items(), key=lambda x: x[1])
            for vaiss in listShip:
                #if not vaiss[0].owner == game_map.get_me():# À priori ce test ne sert à rien
                    command_queue.append(ship.navigate(ship.closest_point_to(vaiss[0]),game_map,speed=int(hlt.constants.MAX_SPEED),ignore_planets=False))
                    logging.debug("Déplacement vers le vaisseau %s" % vaiss[0].id)
                    break
                #else:
                #    logging.debug("Le vaisseau %s est à moi" % vaiss[0].id)
                #    continue
                    
"""1.2.3. Sinon (la planète n'est à personne)"""
"""1.2.3.1. Si peut dock"""
"""1.2.3.1.1. Aller se docker"""
"""1.2.3.2. Sinon"""
"""1.2.3.2.1. Se rapprocher puis docker"""

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
        logging.debug("———")
        logging.debug("Traitement du vaisseau %s" % ship.id)
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            logging.debug("Le vaisseau %s n'est pas en vol" % ship.id)
            # Skip this ship
            continue

        # For each planet in the game (only non-destroyed planets are included)
        
        dictVal={}
        for planet in game_map.all_planets():
            dictVal[planet] = planet.calculate_distance_between(ship)
        listVal = sorted(dictVal.items(), key=lambda x: x[1])
        
        logging.debug("Pour chaque planète")
        for planet in listVal:
            logging.debug("Planète traitée : %s" % planet[0].id)
            #actuel : rien
            #Si peut dock et si la planète est à personne, dock
            logging.debug("Début des conditions")
            if (ship.can_dock(planet[0]) and planet[0].owner == None):
                logging.debug("La planète %s est vide" % planet[0].id)
                command_queue.append(ship.dock(planet[0]))
                logging.debug("Le ship %s peut dock sur la planète précédente" % ship.id)
                break
            
            #Actuel : la planète n'est pas à personne
            #Si peut dock et que la planète est à moi et n'est pas vide
            elif ship.can_dock(planet[0]) or planet[0].owner == game_map.get_me():
                if (planet[0].is_full()):
                    logging.debug("La planète %s est pleine et à moi, planète suivante" % planet[0].id)
                    continue
                else:
                    logging.debug("La planète %s n'est pas pleine" % planet[0].id)
                    command_queue.append(ship.dock(planet[0]))
                    logging.debug("Le ship %s peut dock sur la planète précédente" % ship.id)
                break
            
            #Actuel : la planète est à quelqu'un d'autre
            #Si planète capturée
            elif ship.can_dock(planet[0]) and planet[0].is_owned(): 
                logging.debug("La planète %s est possédée" % planet[0].id)
                dictShip={}
                for vaisseaux in planet[0].all_docked_ships():
                    dictShip[vaisseaux] = vaisseaux.calculate_distance_between(ship)

                listShip = sorted(dictShip.items(), key=lambda x: x[1])
                for vaiss in listShip:
                    if vaiss[0].owner == game_map.get_me():
                        logging.debug("Le vaisseau %s est à moi" % vaiss[0].id)
                        continue
                    else:
                        command_queue.append(ship.navigate(ship.closest_point_to(vaiss[0]),game_map,speed=int(hlt.constants.MAX_SPEED),ignore_planets=False))
                        logging.debug("Déplacement vers le vaisseau %s" % vaiss[0].id)
                    break
                break
            #Actuel : trop loin pour dock, et à personne
            else:
                #navigate_command = 
                logging.debug("Déplacement vers la planète %s" % planet[0].id)
                command_queue.append(ship.navigate(ship.closest_point_to(planet[0]),game_map,speed=int(hlt.constants.MAX_SPEED),ignore_ships=False))
            logging.debug("Fin conditions, passage au vaisseau suivant")
            break
            
#        if navigate_command:
#            command_queue.append(navigate_command)
#        break
        

    # Send our set of commands to the Halite engine for this turn
    logging.debug("     ")
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
