#!/usr/bin/python3.4
from collections import defaultdict
import json
import os
import time
from selenium import webdriver

# adjacency matrix/dictionary read from the map.json
world = []
# firefox webdriver object
driver = []
# configuration
cfg = []


class InitiumMap:
    def __init__(self, file_loc):
        log("Initializing {0}".format(file_loc))
        if os.path.isfile(file_loc):
            with open(file_loc, encoding="utf-8") as data_file:
                self.adj_map = json.loads(data_file.read())
            log("{0} Map locations loaded".format(len(self.adj_map)))
        else:
            print("Error: {0} not found".format(file_loc))

    def check(self):
        log("Checking map for errors")
        error_status = 0

        # check the map for misplaced entries
        # count each path... we should have an even number
        url_count = defaultdict(int)
        path_count = defaultdict(int)
        for path in self.adj_map:
            for adj, url in self.adj_map[path].items():
                url_count[url] += 1
                path_count[path] += 1
                path_count[adj] += 1

        for url, count in url_count.items():
            if count % 2:
                print("{0} has an odd number ({1}) of urls".format(url, count))
                error_status += 1

        for path, count in path_count.items():
            if count == 1:
                print("\"{0}\" is not connected to anything".format(path))
                error_status += 1
            elif count % 2:
                print("\"{0}\" has an odd number ({1}) of paths".
                      format(path, count))
                error_status += 1

        return error_status


def log(txt):
    print("[{0}] {1}".format(time.strftime("%H:%M:%S"), txt))


def init_cfg():
    global cfg

    log("Reading Config")
    if os.path.isfile("cfg.json"):
        with open("cfg.json", encoding="utf-8") as data_file:
            cfg = json.loads(data_file.read())
    else:
        print("Error: cfg.json not found")
        exit(1)


def init_world():
    global world
    world = InitiumMap("map.json")
    err = world.check()
    if err:
        exit(err)


def init_driver():
    log("Initializing webdriver")
    global driver
    driver = webdriver.Firefox()


if __name__ == "__main__":
    init_world()
