# Imports
import discord
from discord.ext import commands
import ibmiotf, ibmiotf.device
import asyncio
from fish import *

###########################################
# Discord API key                         #
# pull token from file not checked in     #
# read one line in case of newline at EOF #
###########################################
DiscordAPI = open("bot-token.txt", "r").readline()[:-1]

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


client = discord.Client()
fishing = fish()

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
	if message.content.startswith(fishTrigger):
		await client.send_message(message.channel, fishing.location(message.author, message.channel))
		await asyncio.sleep(fishing.time(message.author, message.channel))
		await client.send_message(message.channel, fishing.cast(0, 0, 0, 0, 0))
		return

	# Help Message
	if message.content.startswith(helpTrigger):
		f = open(helpF)
		# outputs the main help text file
		await client.send_message(message.channel, f.read())
		f.close()
		return
	# Test Inventory
	if message.content.startswith(invTrigger):
		f = open(invF)
		await client.send_message(message.channel, f.read())
		f.close()
		return
 
# Discord API key
client.run(DiscordAPI)