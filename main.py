import os
import json
import time
import discord
import requests
import configparser
from colorama import *
from discord.ext import commands, tasks
init()

class DiscordBot():
    def __init__(self):
        self.config = []
        self.token = "naw"
        self.apikey = "dang"
        self.intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!', intents=self.intents)
        self.start()
    
    def cls(self): os.system('cls' if os.name == 'nt' else 'clear')
    
    def loadconfig(self):
        if os.path.exists('config.ini') == False:
            print(f'\n   {Fore.LIGHTRED_EX}Config file was not found, creating default one...')
            with open('config.ini', 'w') as configfile:
                configfile.writelines(f'[Main]\ntoken = Discord Token\napi-key = 5sim.net api key')
                configfile.flush()
            print(f'\n   {Fore.LIGHTGREEN_EX}Config file created! - Edit it then press any key.')
            input()

        self.cls()
        print(f'\n   {Fore.LIGHTCYAN_EX}Loading config file!')
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.token = self.config['Main']['token']
        print(self.token)
        self.apikey = self.config['Main']['api-key']
        print(self.apikey)
    
    def checkbal(self):
        headers = {
            'Authorization': f'Bearer {self.apikey}',
            'Accept': 'application/json'
        }

        bal = requests.get('https://5sim.net/v1/user/profile', headers=headers)
        bal = json.loads(bal.text)
        return bal['balance']
    
    def checkprices(self):
        headers = {'Accept': 'application/json'}

        params = (
            ('product', 'discord'),
            ('country', 'england'),
        )

        prices = requests.get('https://5sim.net/v1/guest/prices', headers=headers, params=params).text
        prices = json.loads(prices)
        lycamobile = prices['england']['discord']['lycamobile']['cost']
        virtual34 = prices['england']['discord']['virtual34']['cost']
        return lycamobile, virtual34
    
    async def purchase(self, ctx, country):
        headers = {
            'Authorization': f'Bearer {self.apikey}',
            'Accept': 'application/json',
        }

        channel = self.bot.get_channel(ctx)

        purchased = requests.get(f'https://5sim.net/v1/user/buy/activation/{country}/any/discord', headers=headers).text
        print(purchased)

        if '{"id"' in purchased:
            await channel.send('Order pending...')
            purchasedjson = json.loads(purchased)
            id = purchasedjson['id']
            status = purchasedjson['status']

            if status == 'RECEIVED':
                phone = purchasedjson['phone']
                await channel.send(f'Phone received  (`{id}`)!\nPhone: `{phone}`')

            elif status == 'PENDING':
                for i in range(10):
                    time.sleep(2)
                    checkstatus = requests.get(f'https://5sim.net/v1/user/check/{id}', headers=headers).text
                    checkstatusjson = json.loads(checkstatus)
                    if checkstatusjson['status'] == 'RECEIVED':
                        phone = purchasedjson['phone']
                        await channel.send(f'Phone received  (`{id}`)!\nPhone: `{phone}`')
                        break
            
            tries = 0
            waitingmsg = await channel.send(f'Waiting for code! Tries: `{tries}/900`') 
            for i in range(900):
                time.sleep(1)
                checkstatus = requests.get(f'https://5sim.net/v1/user/check/{id}', headers=headers).text
                checkstatusjson = json.loads(checkstatus)

                if checkstatusjson['sms'] != 'null' and len(checkstatusjson['sms']) != 0:
                    code = checkstatusjson['sms'][0]['code']
                    await channel.send(f'Code received!\nSMS: `{code}`')
                    break

                elif checkstatusjson['sms'] == 'null' or len(checkstatusjson['sms']) == 0:
                    tries +=1
                    await waitingmsg.edit(content=f'Waiting for code! Tries: `{tries}/900`')
    
    async def cancel(self, ctx, id):
        headers = {
            'Authorization': f'Bearer {self.apikey}',
            'Accept': 'application/json',
        }

        channel = self.bot.get_channel(ctx)

        response = requests.get(f'https://5sim.net/v1/user/cancel/{id}', headers=headers).text
        responsejson = json.loads(response)
        phone = responsejson['phone']
        if responsejson['status'] == 'CANCELED':
            await channel.send(f'Phone `{phone}` with ID `{id}` canceled successfully!')
    
    async def ban(self, ctx, id):
        headers = {
            'Authorization': f'Bearer {self.apikey}',
            'Accept': 'application/json',
        }

        channel = self.bot.get_channel(ctx)

        response = requests.get(f'https://5sim.net/v1/user/ban/{id}', headers=headers).text
        responsejson = json.loads(response)
        phone = responsejson['phone']
        if responsejson['status'] == 'BANNED':
            await channel.send(f'Phone `{phone}` with ID `{id}` banned successfully!')

    def startbot(self):
        @self.bot.event
        async def on_ready():
            self.cls()
            print(f'\n   {Fore.LIGHTCYAN_EX}Bot started as {self.bot.user} ({self.bot.user.id}) successfully!')

        @self.bot.command()
        async def bal(ctx):
            await ctx.send(f'Your balance is: {self.checkbal()}')
        
        @self.bot.command()
        async def prices(ctx):
            await ctx.send(f'Lycanmobile price: {self.checkprices()[0]} RUB\nVirtual34 price: {self.checkprices()[1]} RUB')

        @self.bot.command()
        async def purchase(ctx, country):
            await self.purchase(ctx.channel.id, country)
        
        @self.bot.command()
        async def cancel(ctx, id):
            await self.cancel(ctx.channel.id, id)
        
        @self.bot.command()
        async def ban(ctx, id):
            await self.ban(ctx.channel.id, id)
            
        self.bot.run(self.token)

    def start(self):
        self.cls()
        self.loadconfig()
        self.cls()
        self.startbot()

if __name__ == '__main__':
    DiscordBot()