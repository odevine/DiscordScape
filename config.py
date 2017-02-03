import json

# Get config
f = open("config.json", "r").read()
config = json.loads(f)

CONFIG = { 'databaseUrl': config['database-url'],
           'botToken': config['bot-token'],
}
