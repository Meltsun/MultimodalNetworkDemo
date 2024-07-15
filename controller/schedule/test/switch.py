import unittest

from schedule.src.multipath_switch_handle import MultiPathSwitchComposite

class TestUtils(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.switch=MultiPathSwitchComposite()
        
        self.switch.enable_multipath()
    
    def test_register(self):
        self.switch.set_multipath_state((10,1,10),(1,3,2))
        
if __name__ == '__main__':
    unittest.main()