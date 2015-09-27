#!/usr/bin/python3.4
from collections import defaultdict
import json
import sys
import os
import pprint

class Node(dict):
    def __init__(self, name, adj_nodes=[]):
        """
        structure to hold instructions to get to any node from this one
        """
        
        # node name/id
        self.name = name
        
        # don't set the initial generation value
        self.generation = None
        
        # list of immediatly adjacent nodes
        self.adj_nodes = adj_nodes

        # the path to myself from myself is me!
        self[name] = name
        
        for adj_node in self.adj_nodes:
            # mark the adj_nodes nodes
            self[adj_node] = adj_node

    def add_route(self, adj_node, to_node):
        if adj_node not in self.adj_nodes:
            # we have a problem ._.
            print('Error: {0} is not an adj_nodes node in {1}'.format(adj_node, self.name))
        self[to_node] = adj_node


class InitiumMap(dict):
    def __init__(self, file_loc, start='Aera'):
        print('Initializing {0}'.format(file_loc))
        if os.path.isfile(file_loc):
            with open(file_loc, encoding='utf-8') as data_file:
                # TODO: I don't think entries from the adj_map make it into the adj_node lists in the Node class atm
                # It'd be awesome is json.loads would be smart enough to fill Node Objects for me...  
                # I think I want to write a separate fucntion (perhaps standalone?) that converts the adj_map into a InitiumMap
                # And vice-versa.  These are implementations of the same object, but right now, they are just sitting next to each other
                self.adj_map = json.loads(data_file.read())
                self.world = {}
                for loc_1 in self.adj_map:
                    self[loc_1] = Node(loc_1)
            print('{0} Map locations loaded'.format(len(self.adj_map)))
            print('Attempting Solve')
            err = self.check()
            if err:
                sys.exit(err)
            self._solve()
            print('Solved')

        else:
            print('Error: {0} not found'.format(file_loc))

    def check(self):
        print('Checking map for errors')
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
        # for node in self.adj_map:
        #     self.explore()
        # self._explore('5', '5')
        pass

    def _explore(self, parent, node, history=[], generation=0):
        # TODO:
        pass

        
if __name__ == '__main__':

    imap = InitiumMap('map-loop.json')
    pprint.pprint(imap)

    for node in imap.adj_map:
        pass
