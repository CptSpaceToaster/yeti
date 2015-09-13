#!/usr/bin/python3.4
# System
import argparse
import sys
import os
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
# Local
import chat
import world


class Yeti():
    def __init__(self):
        self.cfg = self._parse_config()
        self.world = world.InitiumMap(self.args.map_file)
        # share.init_world()

        print("Initializing webdriver")
        self.driver = webdriver.Firefox()

        print("Connecting to Initium")
        self.driver.get("http://www.playinitium.com")

        print("Logging in as {0}".format(self.cfg["uname"]))
        # Enter email
        printin = self.driver.find_element_by_name("email")
        printin.send_keys(self.cfg["email"])

        # Enter pw
        printin = self.driver.find_element_by_name("password")
        printin.send_keys(self.cfg["pw"])

        for button in self.driver.find_elements_by_class_name(
                "main-button"):
            if button.text == "Login":
                button.click()

        self.chat_helper = chat.ChatBot(self.driver, self.cfg['uname'])

    def _parse_config(self):
        print('Parsing command line arguments')
        self._parser = argparse.ArgumentParser(description="Yeti - A Python based bot for Initium - http://playinitium.com")
        self._parser.add_argument("-c", "--config", dest="config_file", default="cfg.json",
                                  help="Configuration to use (default=cfg.json)")
        self._parser.add_argument("-d", "--do_chat", dest="do_chat", action="store_true",
                                  help="Handle commands in each rooms local chat")
        self._parser.add_argument('-m', '--map', dest='map_file', default='map.json',
                                  help='Map file to use (default=map.json)')
        self.args = self._parser.parse_args()
        print("Reading config")

        if os.path.isfile(self.args.config_file):
            with open(self.args.config_file, encoding="utf-8") as data_file:
                return json.loads(data_file.read())
        else:
            print("Error: Config: {0} not found".format(self.args.config_file))
            sys.exit(1)

    def get_loc(self):
        try:
            elem = self.driver.find_element_by_class_name("header-location")
            if elem:
                if elem.text:
                    return elem.text
        except NoSuchElementException:
            # Not found
            pass

    def get_doge(self):
        elem = self.driver.find_element_by_class_name("header-stats")
        if elem:
            if elem.text:
                stats = elem.text.split()
                if len(stats) > 1:
                    return stats[1]


if __name__ == "__main__":
    try:
        Y = Yeti()
        print("Initializing chatbot")

        print("Current Location: " + Y.get_loc())
        print("        Dogecoin: " + Y.get_doge())

        while True:
            if Y.args.do_chat:
                try:
                    Y.chat_helper.do_chat()
                except NoSuchElementException:
                    # bot missed
                    print("Bot could not find chat entries")
                except UnexpectedAlertPresentException:
                    print("Alerted")

            """
            if Y.get_loc() == 'Aera Inn Basement - South':
                buttons = Y.driver.find_elements_by_class_name("main-button")
                for button in buttons:
                    if '(E)' in button.text:
                        count += 1
                        button.click()
                        break
            time.sleep(1)
            """

    except (ConnectionRefusedError, KeyboardInterrupt) as e:
        if type(e) is KeyboardInterrupt:
            print("")
        if type(e) is ConnectionRefusedError:
            print("Connection to the Firefox Webdriver was lost")
        print("Exiting")
        sys.exit(0)
