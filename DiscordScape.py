# Imports
import discord
import asyncio
import requests
import sys
import handlers
from config import CONFIG
from fish import *

###########################################
# Discord API key                         #
# pull token from config module           #
###########################################
DiscordAPI = CONFIG['botToken']

if len(DiscordAPI) == 0:
    raise IOError("Failed to read token.")

print(DiscordAPI)

#Trigger for Help Command
helpTrigger = '>help'
helpF = "helpFile.txt"
# Trigger for Fishing
fishTrigger = '>fish'
#Trigger for Selling Items
sellTrigger = '>sell'
#Trigger for Inventory
invTrigger = '>inv'
invF = "inventory.txt"

###########################################
# Database API URL                        #
# get base IP from config module          #
###########################################
DATABASE_URL = CONFIG['databaseUrl']

client = discord.Client()

# Bot Ready messages
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Checks Chat for trigger phrase
@client.event
async def on_message(message):

    # If author is the bot itself
    if message.author == client.user:
        return

    # Fishing
    # TODO: place in a handler function outside this file.
    if message.content.startswith(fishTrigger):
        await handlers.fishingTriggerHandler(message, client)

    # Help Message
    if message.content.startswith(helpTrigger):
        f = open(helpF)
        # outputs the main help text file
        await client.send_message(message.channel, f.read())
        f.close()
        return
    # Test Inventory
    if message.content.startswith(invTrigger):
        await handlers.invTriggerHandler(message, client)

# Discord API key
client.run(DiscordAPI)
