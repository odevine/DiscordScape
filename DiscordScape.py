# Imports
import discord
import asyncio
import requests
import sys
import json
from fish import *

# Get config
f = open("config.json", "r").read()
config = json.loads(f)

###########################################
# Discord API key                         #
# pull token from file not checked in     #
# read one line in case of newline at EOF #
###########################################
DiscordAPI = config['bot-token']

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

DATABASE_URL = config['database-url']

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
    # TODO: place in a handler function outside this file.
    if message.content.startswith(fishTrigger):
        #await client.send_message(message.channel, fishing.location(message.author, message.channel))
        await asyncio.sleep(fishing.time(message.author, message.channel))
        # get the fishing result
        fishCaught = fishing.cast(0, 4, 0, 0, 0)
        resp = ""
        # no catch
        if fishCaught is None:
            resp = "Nothing seems to be biting..."
        # caught a fish
        elif fishCaught[2]:
            # response if api call goes well
            resp = "You caught a " + fishCaught[1] + "!"
            try:
                # make the call to /inventory/add/userID/fishID/fishID
                # fishIDs in the dictionary start with F00, need a number starting with 1
                # takes the id, strips the first character, converts to number, adds 1
                r = requests.get(DATABASE_URL + "/inventory/add/" +
                                 message.author.id + "/" + str(int(fishCaught[0][1:]) + 1))
                # in case the server can't process the call
                if r.status_code != requests.codes.ok:
                    resp = "Failed to store the fish in your inventory."
                    # print(fishCaught[0][1:])
            # in case the server is unreachable
            except Exception as e:
                # print debug info
                print(e)
                print(DATABASE_URL + "/inventory/add/" +
                                 message.author.id + "/" + str(int(fishCaught[0][1:]) + 1))
                print(fishCaught[0][1:])
                print(r.status_code)
                resp = "Failed to store the fish in your inventory."
        # fish bit, but got away
        else:
            resp = "The " + fishCaught[1] + " got away..."

        # send the message
        await client.send_message(message.channel, resp)
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
        try:
            r = requests.get(DATABASE_URL + "/inventory/" + message.author.id)
            if r.status_code == requests.codes.ok:
                inv = r.json()
                inventory = "```\n"
                fishes = [f['name'] for f in inv]
                inventoryCellWidth = len(max(fishes, key=len))
                for fish in fishes:
                    inventory += "[{0:{width}}]\n".format(fish, width=inventoryCellWidth)
                inventory += "\n```"
                await client.send_message(message.channel, inventory)
        except ValueError:
            await client.send_message(message.channel,
                                      "Looks like you don't have an inventory yet!")
        except:
            await client.send_message(message.channel, "Sorry, couldn't read your inventory.")
        return

# Discord API key
client.run(DiscordAPI)
