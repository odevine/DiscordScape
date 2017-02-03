import requests
import discord
import asyncio
from config import CONFIG
from fish import *
from collections import Counter

fishing = fish()

DATABASE_URL = CONFIG['databaseUrl']

# handles sending messages
async def invTriggerHandler(message: discord.Message, client: discord.Client):
    try:
        r = requests.get(DATABASE_URL + "/inventory/" + message.author.id)
        if r.status_code == requests.codes.ok:
            # inv = r.json()
            # inventory = "```\n"
            # fishes = [f['name'] for f in inv]
            # inventoryCellWidth = len(max(fishes, key=len))
            # for fish in fishes:
            #     inventory += "[{0:{width}}]\n".format(fish, width=inventoryCellWidth)
            # inventory += "\n```"
            embed = discord.Embed(title=(message.author.display_name + "'s Inventory"),
                                  description="",
                                  colour=discord.Colour.teal())
            embed.set_thumbnail(url=message.author.avatar_url).set_author(name=client.user.name)
            inv = r.json()
            fishes = [f['name'] for f in inv]
            fishCounts = Counter(fishes)
            for key, value in fishCounts.items():
                embed.add_field(name=key, value=value)
            await client.send_message(message.channel, embed=embed)
    # except ValueError:
    #     await client.send_message(message.channel,
    #                               "Looks like you don't have an inventory yet!")
    except Exception as e:
        print(e)
        await client.send_message(message.channel, "Sorry, couldn't read your inventory.")
    return

async def fishingTriggerHandler(message: discord.Message, client: discord.Client):
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
