import unittest

from schedule.src.multipath_switch_handle import MultiPathSwitchComposite

class TestUtils(unittest.TestCase):
    def test_register(self):
        switch=MultiPathSwitchComposite()
        switch.set_multipath_state((5,5,5),(1,2,3))
        
if __name__ == '__main__':
    unittest.main()