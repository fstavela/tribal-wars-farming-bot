from bot import Bot


file = open("profile_path.txt")
path = file.readline()
file.close()

file = open("coords.txt")
coordinates = list(map(str.strip, file.readlines()))
file.close()

troops = {"spy": "1", "light": "1"}

bot = Bot("geckodriver", path)
bot.login("https://www.divoke-kmene.sk/")
bot.go_to_place()
for coords in coordinates:
    bot.attack_village(coords)
