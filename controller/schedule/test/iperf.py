import unittest
from schedule.src.iperf_handle import IperfHandle


class TestIperf(unittest.TestCase):
    def test_config(self):
        handle = IperfHandle(['iperf','-s','-i','1','-p','5000','-u','-e'])
        while True:
            input()
            print("================================================")
            for line in handle.stdout:
                print(repr(str(line)))
                
if __name__ == '__main__':
    unittest.main()