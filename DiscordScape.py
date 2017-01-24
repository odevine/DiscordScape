# Imports
import discord
from discord.ext import commands
import ibmiotf, ibmiotf.device
import asyncio
from fishing import *



# Discord API key
DiscordAPI = 'MjcyNDU4ODA3NzU2NzE4MDgw.C2VSvQ.kcERTwPL3D7MzBvVhFaLYqJRF3I'

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
		await client.send_message(message.channel, fishing.cast(message.author, message.channel))
		await asyncio.sleep(fishing.time(message.author, message.channel))
		await client.send_message(message.channel, fishing.caught(message.author, message.channel))
		return
	# Help Message
	if message.content.startswith(helpTrigger):
		f = open(helpF)
		#outputs the main help text file
		await client.send_message(message.channel, f.read())
		f.close()
		return
	#Test Inventory
	if message.content.startswith(invTrigger):
		f = open(invF)
		await client.send_message(message.channel, f.read())
		f.close()
		return
 
# Discord API key
client.run(DiscordAPI)
