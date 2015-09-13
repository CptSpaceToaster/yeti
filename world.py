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
                self.visited = {}
                self.adj_map = {}
                self.world = {}
                for loc_1 in self.links:
                    self.visited[loc_1] = False
                    self.adj_map[loc_1] = {}
                    for loc_2 in self.links:
                        self.adj_map[loc_1][loc_2] = {}
            print('{0} Map locations loaded'.format(len(self.links)))
            print('Attempting Solve')
            err = self.check()
            if err:
                sys.exit(err)
            self.explore([], start)
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

    def explore(self, parents, node, generation=0):
        self.visited[node] = True
        all_children = []

        # loop to all adjacent paths
        for adj in self.links[node]:
            # print('adj: ' + adj)
            # check to see if we've been there before
            # and if we HAVE been there before, then check the generation
            if not self.visited.get(adj, False) or generation < self.adj_map[adj][adj].get('gen', 0):
                # print('forking to ' + adj)
                # recurse to a child
                children = self.explore(parents + [node], adj, generation+1)[len(parents) + 1:]
                # loop through return'ed list of children nodes
                for child in children:
                    # the path from myself to a child must use the 'adj' token we're looking at
                    self.adj_map[node][child]['path'] = adj

                all_children += children

        # the path from myself to myself is me ._.
        self.adj_map[node][node]['path'] = node
        self.adj_map[node][node]['gen'] = generation

        # print('returning: ')
        # pprint(parents + [node] + all_children)
        # loop through the adjacency map at our current location
        for known_adj in self.adj_map[node]:
            # if the path from myself to the entry in the adjacency map is empty
            # and we have a known parent
            if self.adj_map[node][known_adj].get('path', '') == '' and len(parents) > 0:
                # the path from myself to the empty adj_node must include the last parent
                self.adj_map[node][known_adj]['path'] = parents[-1]

        # Return a list of nodes as-per the generation they were encountered
        return parents + [node] + all_children


if __name__ == '__main__':
    from pprint import pprint

    map = InitiumMap('map-loop.json', '5')
    pprint(map.adj_map)
