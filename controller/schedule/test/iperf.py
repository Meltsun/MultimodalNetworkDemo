import unittest
from schedule.src.iperf_handle import IperfHandle
from schedule.src.utils import iperf_config

class TestIperf(unittest.TestCase):
    def test_config(self):
        handle = IperfHandle(['iperf','-s','-i',iperf_config.interval,'-p',iperf_config.port,'-u','-e'])
        while True:
            input()
            print("================================================")
            for line in handle.stdout:
                print(repr(str(line)))
                
if __name__ == '__main__':
    unittest.main()