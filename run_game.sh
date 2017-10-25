#!/bin/sh

read -p "Effacer les logs et parties précédentes ? (Y/n)" yesno
if [[ $yesno =~ [Nn][Oo]?[Nn]? ]]; then
	rm *.log *.hlt
fi

./halite -d "240 160" "python3 MyBot.py" "python3 MyBot.py"
