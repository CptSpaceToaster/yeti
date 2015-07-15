#!/usr/bin/python3.4
from collections import defaultdict
import os
import json


def check(map_file):
    error_status = 0
    if os.path.isfile(map_file):
        with open(map_file, encoding="utf-8") as data_file:
            adj_map = json.loads(data_file.read())

        # check the map for misplaced entries
        # count each path... we should have an even number
        url_count = defaultdict(int)
        path_count = defaultdict(int)
        for path in adj_map:
            for adj, url in adj_map[path].items():
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
    else:
        err("map.json is missing")

    return error_status


if __name__ == "__main__":
    print("Checking \"map.json\"")
    err = check("map.json")
    if err == 0:
        print("All good!")
    exit(err)
