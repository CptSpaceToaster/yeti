#!/usr/bin/python3.4
import initium_chat
import initium_map
import share
import json
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException


def init():
    share.log("Reading Config")
    if os.path.isfile("cfg.json"):
        with open("cfg.json", encoding="utf-8") as data_file:
            share.cfg = json.loads(data_file.read())
    else:
        print("Error: cfg.json not found")
        exit(1)

    share.log("Initializing Map")
    if os.path.isfile("map.json"):
        with open("map.json", encoding="utf-8") as data_file:
            adj_map = json.loads(data_file.read())
        share.log("{0} Map locations loaded".format(len(adj_map)))
        err = initium_map.check("map.json")
        if err:
            exit(err)

    else:
        print("Error: map.json not found")
        exit(1)

    share.log("Connecting to Initium")
    share.driver = webdriver.Firefox()
    share.driver.get("http://www.playinitium.com")

    share.log("Logging in as {0}".format(share.cfg["uname"]))
    # Enter email
    login = share.driver.find_element_by_name("email")
    login.send_keys(share.cfg["email"])

    # Enter pw
    login = share.driver.find_element_by_name("password")
    login.send_keys(share.cfg["pw"])

    for button in share.driver.find_elements_by_class_name(
            "main-button"):
        if button.text == "Login":
            button.click()

if __name__ == "__main__":
    try:
        init()
        jabber = initium_chat.ChatBot()
        while True:
            try:
                jabber.do_chat()
            except NoSuchElementException:
                # bot missed
                share.log("Bot could not find chat entries")
            except UnexpectedAlertPresentException:
                print("Alerted")

            # Rate Limit
            time.sleep(5)

    except (ConnectionRefusedError, KeyboardInterrupt) as e:
        if type(e) is KeyboardInterrupt:
            print("")
        if type(e) is ConnectionRefusedError:
            share.log("Connection to the Firefox Webdriver was lost")
        share.log("Exiting")
        exit(0)
