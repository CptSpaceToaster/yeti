#!/usr/bin/python3.4
from collections import defaultdict
import json
import sys
import os


class Node():
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


class InitiumMap:
    def __init__(self, file_loc, start='Aera'):
        print('Initializing {0}'.format(file_loc))
        if os.path.isfile(file_loc):
            with open(file_loc, encoding='utf-8') as data_file:
                self.links = json.loads(data_file.read())
                self.adj_map = {}
                self.world = {}
                for loc_1 in self.links:
					# TODO: Implement a dictionary/list of Nodes
					"""
					Node(loc_1, 0, self.links[loc_1].keys())
                    
                    for loc_2 in self.links:
                        self.adj_map[loc_1][loc_2] = {}
                    self.adj_map[loc_1][loc_1]['path'] = loc_1
                    self.adj_map[loc_1][loc_1]['gen'] = 0
                    # self.adj_map[loc_1][loc_1]['gen'] = 999999
					"""
            print('{0} Map locations loaded'.format(len(self.links)))
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
        # for node in self.adj_map:
        pprint(self.links['5'].keys())
        # self._explore('5', '5')

    def _explore(self, parent, node, history=[], generation=0):
        # Check to see if we've been here before indicated by node appearing in 'history' (nodes MUST have unique names)
        if node in history:
            return []
        print('Entering: {0}'.format(node))

        # self.adj_map[parent][node]['gen'] = generation

        all_ancestors = []

        # loop through the adjacent nodes
        for adj_node in self.links[node]:
            # print('HANDELING: {0} on generation: {1}'.format(adj_node, generation))
            # Check to see if we've visited the adj_node before
            if adj_node in history:
                continue

            ancestors, children = self._explore(parent, adj_node, [node] + history, generation+1)
            # children, ancestors = self._explore(parent, adj_node, history + [node], generation+1)

            print('At: {0}    Ancestors: {1}'.format(adj_node, ancestors))
            print('At: {0}    Children: {1}'.format(adj_node, children))

            for child in children:
                self.adj_map[node][child]['path'] = adj_node
                self.adj_map[node][child]['gen'] = generation
                pass

            for ancestor in ancestors:
                # self.adj_map[adj_node][ancestor]['path'] = ancestors[0]
                # self.adj_map[adj_node][ancestor]['gen'] = generation
                # if ancestor not in all_ancestors:
                # all_ancestors.append(child)
                pass

            # self.adj_map[parent][node]['path'] = parent
            # self.adj_map[parent][node]['gen'] = generation
        print()
        return [node] + all_ancestors, history


if __name__ == '__main__':
    from pprint import pprint

    imap = InitiumMap('map-loop.json')
    # pprint(imap.adj_map)

    for node in imap.adj_map:
        pass
