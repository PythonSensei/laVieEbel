#!/bin/sh

read -p "Effacer les logs et parties précédentes ? (Y/n)" yesno
if [[ $yesno =~ [Nn][Oo]?[Nn]? ]]; then
	echo ""
else
	rm *.log *.hlt > /dev/null
fi

./halite -d "240 160" "python3 MyBot.py" "python3 MyBotold.py"
