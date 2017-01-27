import random
import fishDictionaries



# Temp code to show that the player name and location are stored
def loc(player, location):
	output = "Player: %s Location: %s" % (player, location)
	return output

# I, CJ, am too lazy to comment what this does
def time(player, location):
	return 3
	# fuck yeah, 3's a bitchin' number

# Command called when >fish command is used
# Returns the fish that has been caught
def cast(group, sublevel, rodMod, hookMod, baitMod):
	if (biteCheck(baitMod)):
		# Sucessful cast, check for fish or item
		if (fishItemCheck(hookMod)):
			# Catch is a fish, store fish name
			fishID = fishCheck(group, sublevel)
			fishName = fishDictionaries.fishDict.get(fishID)
			# Store modifier
			fishMod = fishDictionaries.fishModDict.get(fishID)

			# Check for success
			if successCheck(rodMod, fishMod, group, sublevel):
				return "You caught a " + fishName + "!"
			else:
				# It gets away...
				return "The " + fishName + " got away..."
		else:
			# Catch item, return item
			return "You caught an [item]!"
	else:
		# Failed cast
		return "Nothing seems to be biting..."

# Checks if sucessful catch
def biteCheck(baitmod):
	# True = Success
	return random.randint(0, 100) > (40 - baitmod)

# Checks if catch is an item or a fish
def fishItemCheck(hookMod):
	# True = Fish
	return random.randint(0, 100) > (20 - hookMod)

# Checks if bite is successful
def successCheck(rodMod, fishMod, group, sublevel):
	# True = caught
	return random.randint(0, 100) < (fishMod + (group * 5) + sublevel) + rodMod

# Determines what fish has been caught
def fishCheck(group, sublevel):
	# If non-recursed
	if (sublevel < 5):
		F0 = 80 - (sublevel * 10)
		F1 = 10 + int((sublevel + 1) / 2) * 5
		F2 = 10 + int(sublevel / 2) * 5
		F3 = sublevel * 5
	# If calculating from a higher group, sublevel 5 will be passed (not normally accessible)
	else : 
		F0 = 10
		F1 = 20
		F2 = 30
		F3 = 40

	# logic behind weighted lists
	fishFind = ["0"] * F0 + ["1"] * F1 + ["2"] * F2 + ["3"] * F3
	fishPick = random.choice(fishFind)

	# if the chosen fish is a 0 of a higher group
	if (fishPick == "0" and group > 0) :
		return fishCheck((group - 1), 5)
	# otherwise return fishID in proper form (ie. F00, F53, etc)
	return "F" + str(group) + fishPick