import yaml
from bot import Bot

file = open("villages.yaml")
farming_data = yaml.safe_load(file)
file.close()

file = open("driver_path.txt")
driver = file.readline().strip()
file.close()

file = open("profile_path.txt")
path = file.readline().strip()
file.close()

bot = Bot(driver, path)
bot.login("https://www.divoke-kmene.sk/")
bot.go_to_place()

for key, value in farming_data["villages"].items():
    if value.keys() is not None and "troops" not in value.keys():
        value["troops"] = farming_data["default"]["troops"]
    if bot.has_enough_troops(value["troops"]["preferred"]):
        bot.attack_village(key, value["troops"]["preferred"])
    elif bot.has_enough_troops(value["troops"]["required"]):
        bot.attack_village(key, value["troops"]["required"])
