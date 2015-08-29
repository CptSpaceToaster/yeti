#!/usr/bin/python3.4
import chat
import share
import time
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException


def init():
    share.init_cfg()
    share.init_world()
    share.init_driver()

    share.log("Connecting to Initium")
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
        share.log("Initializing chatbot")
        jabber = chat.ChatBot()

        share.log("Current Location: " + share.get_loc())
        share.log("        Dogecoin: " + share.get_doge())

        count = 0

        while True:
            if share.args.do_chat:
                try:
                    jabber.do_chat()
                    # Rate Limit
                    time.sleep(5)
                except NoSuchElementException:
                    # bot missed
                    share.log("Bot could not find chat entries")
                except UnexpectedAlertPresentException:
                    print("Alerted")

            if share.get_loc() == 'Aera Inn Basement - South':
                buttons = share.driver.find_elements_by_class_name("main-button")
                for button in buttons:
                    if '(E)' in button.text:
                        count += 1
                        button.click()
                        break
            time.sleep(1)

    except (ConnectionRefusedError, KeyboardInterrupt) as e:
        if type(e) is KeyboardInterrupt:
            print("")
        if type(e) is ConnectionRefusedError:
            share.log("Connection to the Firefox Webdriver was lost")
        share.log("Exiting")
        share.log('Number of times explore was pressed: ' + str(count))
        sys.exit(0)
