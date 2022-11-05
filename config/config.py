import yaml

with open("config.yaml", "r") as config_file:
    CONFIG_FILE = yaml.load(config_file, Loader=yaml.Loader)

BOT_CONFIG = CONFIG_FILE["BOT"]
BOT_TOKEN = BOT_CONFIG["TOKEN"]
