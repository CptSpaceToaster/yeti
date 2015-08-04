#!/usr/bin/python3.4
import datetime
import json
import share
import pytz
import random
import requests
from tzlocal import get_localzone


class ChatMessage:
    def __init__(self, element):
        # Attempt to parse the timestamp from the element, and convert it to GMT
        # Get the message time Title
        date = element.find_element_by_class_name("chatMessage-time").get_attribute("title")
        # Append the text from that element, to form a date-string
        date += element.find_element_by_class_name("chatMessage-time").text
        # Parse the date-string into a datetime object
        self.gmt_dt = datetime.datetime.strptime(date, "%A, %B %d, %Y[%H:%M]")
        # set the datetime object to GMT
        self.gmt_dt = pytz.timezone("GMT").localize(self.gmt_dt)

        # Obtain the Username and Text from the message-text
        elems = element.find_elements_by_class_name("chatMessage-text")
        # If we have more than one element, username and text were combined (usually when the user typed /me [text]
        if len(elems) > 1:
            self.user = elems[0].text
            self.text = elems[1].text
        # Otherwise, the message-text and username are separated nicely
        else:
            self.text = elems[0].text
            self.user = element.find_element_by_class_name(
                "chatMessage-nickname").text

    # Define behavior for equivalence
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

        share.log("Calculating timezone")
        # Set current time to whatever the system time is
        self.tz = get_localzone()
        self.local_dt = self.tz.localize(datetime.datetime.now())
        # Send the bot back in time 1 minute, to detect lines on startup
        self.local_dt -= datetime.timedelta(minutes=1)
        # Convert to GMT
        self.gmt_dt = self.local_dt.astimezone(pytz.timezone("GMT"))

    def do_chat(self):
        elements = share.driver.find_elements_by_class_name(
            "chatMessage-main")
        for_later = []

        # Iterate top down, to skim off the new messages
        for elem in elements:
            msg = ChatMessage(elem)

            # check if we've seen this message before
            if msg == self.last_msg:
                break
            # prevent recursion
            if msg.user == share.cfg["uname"]:
                break
            # check to see if the message is new, compared when the bot was initialized
            if msg.gmt_dt < self.gmt_dt:
                break
            # Save them for later, beacuse we want to process them backwards
            # (as they happened in real time)
            for_later.insert(0, msg)

        # keep track of the last parsed message, and use it as a "stopping point"
        if len(elements) > 0:
            self.last_msg = ChatMessage(elements[0])

        # Iterate through all of the new messages
        for msg in for_later:
            # Check to see if the message has content
            if msg.text:
                share.log(msg.user + ": " + msg.text)
                slack_msg(msg.user, msg.text)

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
        # Handle a couple of basic commands
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
        # Enter text in the chat box, and hit enter!
        chat = share.driver.find_element_by_id("chat_input")
        chat.send_keys(text)
        chat.submit()


def slack_msg(usr, txt):
    # Post a message to slack (if it's enabled at startup with --slack)
    if share.args.slack_enabled:
        # Create the content we want to send to slack, via incoming webhook
        payload = {'channel': share.cfg["slack_channel"],
                   'username': usr,
                   'text': txt,
                   'icon_emoji': share.cfg["slack_icon_emoji"]
                   }

        # Slack accepts json payloads
        headers = {'content-type': 'application/json'}

        # shipit.jpg
        r = requests.post(share.cfg["slack_url"], data=json.dumps(payload), headers=headers)
        if r.status_code != 200:
            share.log("Error: " + str(r.status_code) + " " + r.reason + " - " + r.text)
