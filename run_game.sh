#!/bin/sh

read -p "Effacer les logs et parties précédentes ? (y/N)" yesno
if [[ $yesno =~ [Yy][Ee]?[Ss]? ]]; then
	rm *.log *.hlt
fi

./halite -d "240 160" "python3 MyBot.py" "python3 MyBot.py"
