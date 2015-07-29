#!/usr/bin/python3.4
import argparse
from collections import defaultdict
import json
import os
import time
from selenium import webdriver
from pprint import pprint

parser = argparse.ArgumentParser(description="Yeti - A Python based bot for Initium - http://playinitium.com")
parser.add_argument("-s", "--slack", dest="slack_enabled", action="store_true",
                    help="Fork all of the logged messages to a slack incoming webhook (default=false)")
parser.add_argument("-c", "--config", dest="config_file", default="cfg.json",
                    help="Configuration to use (default=cfg.json)")
args = parser.parse_args()


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
                self.links = json.loads(data_file.read())
                self.visited = {}
                self.adj_map = {}
                for key in self.links:
                    self.visited[key] = False
                    self.adj_map[key] = {}
                    for k in self.links:
                        self.adj_map[key][k] = ""
            log("{0} Map locations loaded".format(len(self.links)))
        else:
            print("Error: {0} not found".format(file_loc))

    def check(self):
        log("Checking map for errors")
        error_status = 0

        # check the map for misplaced entries
        # count each path... we should have an even number
        url_count = defaultdict(int)
        path_count = defaultdict(int)
        for path in self.links:
            for adj, url in self.links[path].items():
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

    def solve(self):
        log("Attempting Solve")
        self.explore([], "Aera")
        log("Solved")

    def explore(self, parents, node):
        self.visited[node] = True
        all_children = []

        for adj in self.links[node]:
            # print("adj: " + adj)
            if not self.visited.get(adj, False):
                # print("forking to " + adj)
                children = self.explore(parents + [node],
                                        adj)[len(parents) + 1:]
                for child in children:
                    self.adj_map[node][child] = adj

                all_children += children

        self.adj_map[node][node] = node

        # print("returning: ")
        # pprint(parents + [node] + all_children)
        for key in self.adj_map[node]:
            if self.adj_map[node][key] == "":
                if len(parents) > 0:
                    self.adj_map[node][key] = parents[-1]
        return parents + [node] + all_children


def log(txt):
    print("[{0}] {1}".format(time.strftime("%H:%M:%S"), txt))


def init_cfg():
    global cfg

    log("Reading Config")
    if os.path.isfile(args.config_file):
        with open(args.config_file, encoding="utf-8") as data_file:
            cfg = json.loads(data_file.read())
    else:
        print("Error: " + args.config_file + " not found")
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
    world.solve()
    pprint(world.adj_map)
