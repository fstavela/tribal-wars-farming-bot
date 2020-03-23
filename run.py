from bot import Bot


file = open("driver_path.txt")
driver = file.readline().strip()
file.close()

file = open("profile_path.txt")
path = file.readline().strip()
file.close()

file = open("coords.txt")
coordinates = list(map(str.strip, file.readlines()))
file.close()

troops = {"spy": "1", "light": "1"}

bot = Bot(driver, path)
bot.login("https://www.divoke-kmene.sk/")
bot.go_to_place()
for coords in coordinates:
    if coords:
        bot.attack_village(coords, troops)
