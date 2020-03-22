from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from random import randint


class Bot:
    def __init__(self, gecko_path, profile_path=None):
        profile = webdriver.FirefoxProfile(profile_path) if profile_path else webdriver.FirefoxProfile()
        self.browser = webdriver.Firefox(executable_path=gecko_path, firefox_profile=profile)
        self.place = False
        self.logged = False

    def login(self, url, world=None):
        self.browser.get(url)

        xpath = "//span[@class='world_button_active'"
        if world:
            xpath += f" and contains(@text, {world})"
        xpath += "]"

        world_button_element = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        sleep(randint(15, 25) / 10)
        world_button_element.click()
        sleep(randint(15, 25) / 10)

        self.logged = True

    def go_to_place(self, village_id):
        xpath = "//div[contains(@class, 'visual-label-place')]"
        place_element = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        place_element.click()
