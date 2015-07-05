#!/usr/bin/python3.4
import time
import random
import configparser
from selenium import webdriver

driver = webdriver.Firefox()
config = configparser.ConfigParser()


class ChatMessage:
    def __init__(self, element):
        date = element.find_element_by_class_name("chatMessage-time") \
            .get_attribute("title")
        date += element.find_element_by_class_name("chatMessage-time").text
        self.stamp = time.mktime(time.strptime(date, "%A, %B %d, %Y[%H:%M]"))

        elems = element.find_elements_by_class_name("chatMessage-text")
        if len(elems) > 1:
            self.user = elems[0].text
            self.text = elems[1].text
        else:
            self.text = elems[0].text
            self.user = element.find_element_by_class_name("chatMessage \
                    -nickname").text

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.stamp == other.stamp and self.user == other.user \
                and self.text == other.text
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ChatBot:
    def __init__(self):
        self.msg = None
        self.last_msg = None
        # Fudge factor for different timezones
        self.epoch = time.time() + 14400
        print("Initialized Chatbot")

    def do_chat(self):
        global driver
        global config
        self.last_msg = self.msg
        self.msg = ChatMessage(driver.find_element_by_class_name("chatMessage \
            -main"))

        # prevent recursion
        if (self.msg.user == config.get("Credentials", "uname")):
            return
        if (self.last_msg != self.msg):
            if (self.msg.stamp < self.epoch):
                return

            print(self.msg.user + " " + self.msg.text)

            if self.msg.text[0] == "!":
                tokens = self.msg.text.split()
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


def init():
    global driver
    global config
    print("Reading Config")
    config.read("cfg.ini")

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
    init()
    jabber = ChatBot()
    while True:
        jabber.do_chat()
        # Rate Limit
        time.sleep(5)
