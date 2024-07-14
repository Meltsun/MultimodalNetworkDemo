import unittest

from schedule.src.multipath_switch_handle import MultiPathSwitchComposite

class TestUtils(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.switch=MultiPathSwitchComposite()
        
    
    def test_register(self):
        self.switch.set_multipath_state((4,5,6),(1,2,3))
        
if __name__ == '__main__':
    unittest.main()