#!/usr/bin/python3.4
# System
import argparse
import sys
import os
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
# Local
import chat
import world
import initium


class Yeti(initium.webdriver):
    def __init__(self):
        self.cfg = self._parse_config()
        self.world = world.InitiumMap(self.args.map_file)

        print("Initializing webdriver")
        # Hax
        super().__init__()

        print("Connecting to Initium")
        self.get("http://www.playinitium.com")

        print("Logging in as {0}".format(self.cfg["uname"]))
        # Enter email
        login = self.find_element_by_name("email")
        login.send_keys(self.cfg["email"])

        # Enter pw
        login = self.find_element_by_name("password")
        login.send_keys(self.cfg["pw"])

        for button in self.find_elements_by_class_name(
                "main-button"):
            if button.text == "Login":
                button.click()

        self.chat_helper = chat.ChatBot(self, self.cfg['uname'])

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


if __name__ == "__main__":
    try:
        Y = Yeti()
        print("Initializing chatbot")

        print("Current Location: " + Y.get_location())
        print("        Dogecoin: " + Y.get_gold())

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
                buttons = Y.find_elements_by_class_name("main-button")
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
