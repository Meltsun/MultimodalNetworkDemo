import unittest

class TestUtils(unittest.TestCase):
    def test_config(self):
        from schedule.src.utils import switch_configs
        print(switch_configs)
        
if __name__ == '__main__':
    unittest.main()