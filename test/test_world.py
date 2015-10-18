#!/usr/bin/env python3.4
# System
import unittest
import json
import tempfile
import os
import errno

# Local
from initium import world


def get_temp_filename(dir=None, pre=None, suf=''):
    """
    ARRRRRRRR
    This be cobbled together from stolen pieces of tempfile
    """
    if dir is None:
        dir = tempfile.gettempdir()
    if pre is None:
        pre = tempfile.gettempprefix()

    # Obtain the names iterator
    names = tempfile._get_candidate_names()

    for seq in range(tempfile.TMP_MAX):
        ret = os.path.join(dir, pre + next(names) + suf)
        if os.path.exists(ret):
            continue
        return ret
    raise FileExistsError(errno.EEXIST,
                          'No usable temporary file name found')


class InitiumMapFileTest(unittest.TestCase):
    def setUp(self):
        self.map_name = get_temp_filename(suf='.json')

        # A map!
        self.test_map = {
            '1': {
                '2': '2'
            },
            '2': {
                '1': '1'
            }
        }

    def test_load(self):
        # Manually store data in file
        with open(self.map_name, 'w') as tmp:
            json.dump(self.test_map, tmp, indent=4, sort_keys=True)
        # Load from a file using the constructor
        M = world.InitiumMapFile(self.map_name)
        self.assertEqual(M, self.test_map)

    def test_save(self):
        M = world.InitiumMapFile(self.map_name, self.test_map)
        # Check that we constructed the map properly
        self.assertEqual(M, self.test_map)
        M.save()
        # Check the file contents
        with open(self.map_name, 'r') as tmp:
            self.assertEqual(json.load(tmp), self.test_map)

    def test_reload(self):
        M = world.InitiumMapFile(self.map_name, self.test_map)
        # Check that we constructed the map properly
        self.assertEqual(M, self.test_map)
        M.save()
        M['3'] = 'foo'
        self.assertIn('3', M)
        M.load()
        self.assertNotIn('3', M)

    def tearDown(self):
        os.unlink(self.map_name)


if __name__ == '__main__':
    unittest.main()
