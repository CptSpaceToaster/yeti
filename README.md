yeti
----

A python based bot for [initium](http://playinitium.com/).

##Dependencies
This bot was written using python3.4, and uses a firefox webdriver and selenium to intertact with dynamic webpages
```
sudo apt-get install firefox
sudo pip3 install selenium pytz tzlocal
```

##Config File
You will need a config in the directory you run the bot.  It must be named `cfg.json`

Example `cfg.json`
```
{
    "email": "your-email@your.domain.com",
    "uname": "YourUsername",
    "pw": "YourPassword"
}
```

##Running
```
./yeti.py -h
./yeti.py
```

If you want to fork the bot's logged messages to a slack incoming webhook, you will need to add 4 more entries to your config file:

```
{
    "email": "your-email@your.domain.com",
    "uname": "YourUsername",
    "pw": "YourPassword",
    "slack_url": "https://hooks.slack.com/services/your/secret/token",
    "channel": "#channel-name",
    "username": "Username",
    "icon_emoji": ":ghost:"
}
```

Tell the bot to output messages with the `--slack` flag
```
./yeti.py --slack
```
