# Imports
import discord
from discord.ext import commands
import ibmiotf, ibmiotf.device
import asyncio

# Discord API key
DiscordAPI = 'MjcyNDU4ODA3NzU2NzE4MDgw.C2VSvQ.kcERTwPL3D7MzBvVhFaLYqJRF3I'

#Trigger for Help Command
helpTrigger = '>help'
# Trigger for Fishing
fishTrigger = '>fish'
#Trigger for Selling Items
sellTrigger = '>sell'



output = ""
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
    # If the message starts with the trigger
    if message.content.startswith(fishTrigger):
        await client.send_message(message.channel, "You attempt to fish...")
        return
    if message.content.startswith(helpTrigger):
    	await client.send_message(message,channel, "```How can I help? /n Test```")
        return
 
# Discord API key
client.run(DiscordAPI)
