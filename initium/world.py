#!/usr/bin/python3.4
from collections import defaultdict
import json
import os


"""
class MapFieldException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
"""


class InitiumNode(dict):
    def __init__(self, name, generation, adjacent=[]):
        self.name = name
        self.generation = generation

        # immediatly adjacent nodes
        self.adjacent = adjacent

        # structure to hold instructions to get to any node from this one
        self.route = {}

        # the path to myself from myself is me!
        self.route[name] = name

        for adj_node in self.adjacent:
            # mark the adjacent nodes
            self.route[adj_node] = adj_node

    def add_route(self, adj_node, to_node):
        if adj_node not in self.adjacent:
            # we have a problem ._.
            print('Error: {0} is not an adjacent node in {1}'.format(adj_node, self.name))
        self.route[to_node] = adj_node


class InitiumMap(dict):
    def __init__(self, *args, start='Aera', **kwargs):
        super().__init__(*args, **kwargs)

    def check(self):
        print('Checking map for errors')
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
                print('{0} has an odd number ({1}) of urls'.format(url, count))
                error_status += 1

        for path, count in path_count.items():
            if count == 1:
                print('\'{0}\' is not connected to anything'.format(path))
                error_status += 1
            elif count % 2:
                print('\'{0}\' has an odd number ({1}) of paths'.format(path, count))
                error_status += 1

        return error_status

    def _solve(self):
        pass

    def _explore(self, parent, node, history=[], generation=0):
        pass


class InitiumMapFile(InitiumMap):
    def __init__(self, file_loc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_loc = file_loc

        # If no arguments were provided, then assume the file is a map to be opened
        if not args and not kwargs:
            if os.path.isfile(file_loc):
                self.load()
        else:
            if not os.path.isfile(file_loc):
                self.save()
            else:
                raise FileExistsError

    def load(self):
        with open(self.file_loc, 'r') as data_file:
            # Clean out the old entries in the dict
            super().clear()
            # Load new ones
            super().update(json.load(data_file))

    def save(self):
        with open(self.file_loc, 'w') as data_file:
            json.dump(self, data_file, indent=4, sort_keys=True)
