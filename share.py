#!/usr/bin/python3.4
import time

# adjacency matrix/dictionary read from the map.json
adj_map = []
# firefox webdriver object
driver = []
# configuration
cfg = []


def log(txt):
        print("[{0}] {1}".format(time.strftime("%H:%M:%S"), txt))
