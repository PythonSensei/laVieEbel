#!/bin/bash 

curr=`pwd`
zip mybot.zip ./hlt/ ./MyBot.py
mv mybot.zip /home/$USER/Documents/Dev/hlt_client/
cd "$curr/../hlt_client/"
python client.py bot -b mybot.zip
rm mybot.zip
cd $curr
exit 0
