#!/usr/bin/python3.4
from collections import defaultdict
import json
import os


class InitiumMap:
    def __init__(self, file_loc):
        print('Initializing {0}'.format(file_loc))
        if os.path.isfile(file_loc):
            with open(file_loc, encoding='utf-8') as data_file:
                self.links = json.loads(data_file.read())
                self.visited = {}
                self.adj_map = {}
                self.world = {}
                for key in self.links:
                    self.visited[key] = False
                    self.adj_map[key] = {}
                    for k in self.links:
                        self.adj_map[key][k] = ''
            print('{0} Map locations loaded'.format(len(self.links)))
            self._solve()
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
        print('Attempting Solve')
        self.explore([], 'Aera')
        print('Solved')

    def explore(self, parents, node):
        self.visited[node] = True
        all_children = []

        for adj in self.links[node]:
            # print('adj: ' + adj)
            if not self.visited.get(adj, False):
                # print('forking to ' + adj)
                children = self.explore(parents + [node], adj)[len(parents) + 1:]
                for child in children:
                    self.adj_map[node][child] = adj

                all_children += children

        self.adj_map[node][node] = node

        # print('returning: ')
        # pprint(parents + [node] + all_children)
        for key in self.adj_map[node]:
            if self.adj_map[node][key] == '':
                if len(parents) > 0:
                    self.adj_map[node][key] = parents[-1]
        return parents + [node] + all_children


if __name__ == '__main__':
    from pprint import pprint

    map = InitiumMap('map.json')
    pprint(map.adj_map)
