import unittest

class TestUtils(unittest.TestCase):
    def test_config(self):
        from schedule.src.utils import switch_config
        print(switch_config)
        
if __name__ == '__main__':
    unittest.main()