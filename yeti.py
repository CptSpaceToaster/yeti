#!/usr/bin/python3.4
import datetime
import json
import random
import os
import pytz
import time
from tzlocal import get_localzone
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException

# firefox webdriver
global driver
# configuration values
global cfg
# adjacency matrix/dictionary read from the map.json
global adj_map

class ChatMessage:
    def __init__(self, element):
        # Date Parser
        date = element.find_element_by_class_name("chatMessage-time") \
            .get_attribute("title")
        date += element.find_element_by_class_name("chatMessage-time").text
        self.gmt_dt = datetime.datetime.strptime(date, "%A, %B %d, %Y[%H:%M]")
        self.gmt_dt = pytz.timezone("GMT").localize(self.gmt_dt)

        elems = element.find_elements_by_class_name("chatMessage-text")
        if len(elems) > 1:
            self.user = elems[0].text
            self.text = elems[1].text
        else:
            self.text = elems[0].text
            self.user = element.find_element_by_class_name(
                "chatMessage-nickname").text

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.gmt_dt == other.gmt_dt and self.user == other.user \
                and self.text == other.text
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ChatBot:
    def __init__(self):
        self.last_msg = None

        log("Calculating Timezone")
        self.tz = get_localzone()
        self.local_dt = self.tz.localize(datetime.datetime.now())
        # Send the bot back in time 1 minute, to detect lines on startup
        self.local_dt -= datetime.timedelta(minutes=1)
        self.gmt_dt = self.local_dt.astimezone(pytz.timezone("GMT"))
        log("Initialized Chatbot")

    def do_chat(self):
        global driver
        global cfg

        elements = driver.find_elements_by_class_name(
            "chatMessage-main")
        for_later = []

        # Iterate top down, to skim off the new messages
        for elem in elements:
            msg = ChatMessage(elem)

            # check if the message is old
            if msg == self.last_msg:
                break
            # prevent recursion
            if msg.user == cfg["uname"]:
                break
            if msg.gmt_dt < self.gmt_dt:
                break
            # Save them for later, beacuse we want to process them backwards
            # (as they happened in real time)
            for_later.insert(0, msg)

        if len(elements) > 0:
            self.last_msg = ChatMessage(elements[0])

        # Iterate through all of the new messages
        for msg in for_later:
            log(msg.user + ": " + msg.text)

            if msg.text[0] == "!":
                tokens = msg.text.split()
                n = len(tokens)

                cmd = tokens[0][1:]
                if n > 1:
                    args = tokens[1:]
                else:
                    args = []

                self.handle(cmd, args, n)

    def handle(self, cmd, args, n):
        if cmd == "help":
            self.respond("Available commands: help, bot-say [TEXT], \
                    roll [NUM]")
        if cmd == "bot-say":
            self.respond(" ".join(args))
        if cmd == "roll":
            try:
                i = int(args[0])
                if i > 0:
                    self.respond(str(random.randrange(0, i) + 1))
                else:
                    self.respond("Error: Integer is not greater than zero")
            except ValueError:
                self.respond("Error: Roll needs an Positive Integer Argument")

    def respond(self, text):
        global driver
        chat = driver.find_element_by_id("chat_input")
        chat.send_keys(text)
        chat.submit()


def log(txt):
    print("[{0}] {1}".format(time.strftime("%H:%M:%S"), txt))


def init():
    global driver
    global cfg
    global adj_map

    log("Reading Config")
    if os.path.isfile("cfg.json"):
        with open("cfg.json", encoding="utf-8") as data_file:
            cfg = json.loads(data_file.read())
    else:
        print("Error: cfg.json not found")
        exit(1)

    log("Initializing Map")
    if os.path.isfile("map.json"):
        with open("map.json", encoding="utf-8") as data_file:
            adj_map = json.loads(data_file.read())
        log("{0} Map locations loaded".format(len(adj_map)))
    else:
        print("Error: map.json not found")
        exit(1)

    log("Connecting to Initium")
    driver = webdriver.Firefox()
    driver.get("http://www.playinitium.com")

    log("Logging in as {0}".format(cfg["uname"]))
    # Enter email
    login = driver.find_element_by_name("email")
    login.send_keys(cfg["email"])

    # Enter pw
    login = driver.find_element_by_name("password")
    login.send_keys(cfg["pw"])

    for button in driver.find_elements_by_class_name("main-button"):
        if button.text == "Login":
            button.click()

if __name__ == "__main__":
    try:
        init()
        jabber = ChatBot()
        while True:
            try:
                jabber.do_chat()
                # Rate Limit
            except NoSuchElementException:
                # bot missed
                log("Bot could not find chat entries")
            except UnexpectedAlertPresentException:
                print("Alerted")

            time.sleep(5)
    
    except (ConnectionRefusedError, KeyboardInterrupt) as e:
        if type(e) is KeyboardInterrupt:
            print("")
        if type(e) is ConnectionRefusedError:
            log("Connection to the Firefox Webdriver was lost")
        log("Exiting")
        exit(0)

