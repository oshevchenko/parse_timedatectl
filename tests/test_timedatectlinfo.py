import unittest
from unittest.mock import Mock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
# from mq4hemc import HemcMessage, HemcMessageDict, HemcTick, getNotifier
import time
from timedateinfo import TimeDateInfo

class TestTimeDateInfo(unittest.TestCase):
    def test_file_parser(self):
        timedatectl_output_path = os.path.join(os.path.dirname(__file__), 'timedatectl_output.txt')
        with open(timedatectl_output_path, 'r') as f:
            timedatectl_output = f.read()
        timedateinfo = TimeDateInfo()
        parsed_dict = timedateinfo.parse_timedatectl_output(timedatectl_output)
        # print(parsed_dict)
        self.assertEqual(parsed_dict['timezone'], 'Europe/Kiev')
        self.assertEqual(parsed_dict['timezone_c'], 'Europe/Kiev (EEST, +0300)')
        self.assertEqual(parsed_dict['local_time'], '2025-05-19 16:01:35')
        self.assertEqual(parsed_dict['universal_time'], '2025-05-19 13:01:35')
        self.assertEqual(parsed_dict['system_clock_sync'], 'yes')


if __name__ == "__main__":
    unittest.main()
