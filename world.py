#!/usr/bin/python3.4
from collections import defaultdict
import json
import sys
import os


class InitiumMap:
    def __init__(self, file_loc, start='Aera'):
        print('Initializing {0}'.format(file_loc))
        if os.path.isfile(file_loc):
            with open(file_loc, encoding='utf-8') as data_file:
                self.links = json.loads(data_file.read())
                self.adj_map = {}
                self.world = {}
                for loc_1 in self.links:
                    self.adj_map[loc_1] = {}
                    for loc_2 in self.links:
                        self.adj_map[loc_1][loc_2] = {}
                    self.adj_map[loc_1][loc_1]['path'] = loc_1
                    # self.adj_map[loc_1][loc_1]['gen'] = 999999
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
        self._explore('5', '5')

    def _explore(self, parent, node, history=[], generation=0):
        # Check to see if we've been here before indicated by node appearing in 'history' (nodes MUST have unique names)
        if node in history:
            return []
        print('Entering: {0}'.format(node))

        self.adj_map[parent][node]['gen'] = generation

        # loop through the adjacent nodes
        for adj_node in self.links[node]:
            # Check the generation value to see if we should walk in that direction
            if generation < self.adj_map[parent][adj_node].get('gen', 999999):
                # print('Forking into: {0}'.format(adj_node))
                ancestors = self._explore(parent, adj_node, history + [node], generation+1)
                print('At: {0}    Ancestors: {1}'.format(adj_node, ancestors))

                for ancestor in ancestors:
                    self.adj_map[adj_node][ancestor]['path'] = ancestors[0]
                    pass

            # self.adj_map[parent][node]['path'] = parent
            # self.adj_map[parent][node]['gen'] = generation
        print()
        return history + [node]


if __name__ == '__main__':
    from pprint import pprint

    imap = InitiumMap('map-loop.json')
    pprint(imap.adj_map)

    for node in imap.adj_map:
        pass
