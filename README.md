# 5sim-discord-bot
Discord bot to buy phones using 5sim api (Discord phones)


#Setup:
- Install requirements `pip install -r requirements.txt`
- Run main.py `py main.py`
- Wait for the program to create the config for you
- Go to discord developer portal and get the bot token
- Go to 5sim.net and get your api key (The long one)
- Edit the config (config.ini)
- Ready to use!

#Commands:
- !bal - Sends account balance
- !prices - Sends prices for discord phones
- !purchase (country) - Buys a discord phone number - Need to specify country (England or netherlands recommended)
- !cancel (id) - Cancels an order - Need to specify order id (can be found when using purchase command)
- !ban (id) - Bans an order (When the phone is banned from discord) - Need to specify order id (can be found when using purchase command)
