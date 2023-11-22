from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint


class Bot:
    def __init__(self, gecko_path, profile_path=None):
        profile = webdriver.FirefoxProfile(profile_path) if profile_path else webdriver.FirefoxProfile()
        service = Service(executable_path=gecko_path)
        options = Options()
        options.add_argument("-profile")
        options.add_argument(profile.path)
        self.browser = webdriver.Firefox(service=service, options=options)
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

    def go_to_place(self):
        if not self.logged:
            raise Exception("Bot is not logged in")

        # Check for captcha
        while self._element_exists("//div[@id='bot_check']"):
            sleep(10)

        xpath = "//div[contains(@class, 'visual-label-place')]"
        place_element = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        place_element.click()

        self.place = True

    def attack_village(self, coords, troops):
        if not self.place:
            self.go_to_place()
        if not self.has_enough_troops(troops):
            raise Exception("Doesn't have enough troops")

        # Check for captcha
        while self._element_exists("//div[@id='bot_check']"):
            sleep(10)

        self._clear_troops_inputs()

        # Set coordinates value
        xpath = "//div[@id='place_target']/input"
        coords_element = self.browser.find_element("xpath", xpath)
        coords_element.send_keys(coords)
        sleep(randint(4, 10) / 10)

        # Set troops values for all troop types
        for key, value in troops.items():
            xpath = f"//input[@id='unit_input_{key}']"
            army_element = self.browser.find_element("xpath", xpath)
            army_element.send_keys(str(value))
            sleep(randint(4, 10) / 10)

        # Click on the "Attack" button on the place page
        xpath = "//input[@id='target_attack']"
        button_element = self.browser.find_element("xpath", xpath)
        button_element.click()
        sleep(randint(15, 25) / 10)

        # Check for captcha
        while self._element_exists("//div[@id='bot_check']"):
            sleep(10)

        # Check for error
        if self._element_exists("//div[@class='error_box']"):
            xpath = "//div[@class='village-item']"
            if self._element_exists(xpath):
                self.browser.find_element("xpath", xpath).click()
            return False

        # Click on the "Attack button on the confirmation page
        xpath = "//input[contains(@class, 'btn-attack')]"
        attack_element = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        attack_element.click()
        sleep(randint(15, 25) / 10)

        return True

    def has_enough_troops(self, troops):
        if not self.place:
            self.go_to_place()

        # Check for captcha
        while self._element_exists("//div[@id='bot_check']"):
            sleep(10)

        for key, value in troops.items():
            xpath = f"//a[@id='units_entry_all_{key}']"
            amount_element = self.browser.find_element("xpath", xpath)
            amount = int(amount_element.text.strip("() \n"))
            if amount < int(value):
                return False

        return True

    def _element_exists(self, xpath):
        try:
            self.browser.find_element("xpath", xpath)
        except NoSuchElementException:
            return False
        return True

    def _clear_troops_inputs(self):
        fields = self.browser.find_elements("xpath", "//input[@class='unitsInput']")
        for field in fields:
            if field.get_property("value"):
                field.clear()
                sleep(randint(4, 10) / 10)

    def __del__(self):
        self.browser.quit()
