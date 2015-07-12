#!/usr/bin/python3.4
import configparser
import datetime
import random
import pytz
import time
from tzlocal import get_localzone
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Firefox()
config = configparser.ConfigParser()


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
        global config

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
            if msg.user == config.get("Credentials", "uname"):
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
    print(str("[" + time.strftime("%H:%M:%S")) + "] " + txt)


def init():
    global driver
    global config
    # TODO: Error if config is missing
    log("Reading Config")
    config.read("cfg.ini")
    log("Connecting to Initium")
    driver.get("http://www.playinitium.com")

    # Enter email
    login = driver.find_element_by_name("email")
    login.send_keys(config.get("Credentials", "email"))

    # Enter pw
    login = driver.find_element_by_name("password")
    login.send_keys(config.get("Credentials", "pw"))

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

            time.sleep(5)

    except KeyboardInterrupt:
        print("")
        log("Exiting")
        exit(0)
