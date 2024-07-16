import unittest
from schedule.src.iperf_handle import IperfHandle
from schedule.src.utils import iperf_config,root
import traceback

class TestIperf(unittest.TestCase):
    def setUp(self) -> None:
        self.handle = IperfHandle(['iperf','-s','-i',iperf_config.interval,'-p',iperf_config.port,'-u','-e'])
                
    def test_phase(self):
        log_path = root/"test"/"iperf.log"
        for i,line in enumerate(log_path.open()):
            try:
                res = self.handle.phase_line(line)
                if res is None:
                    raise Exception(f"第{i}行未解析")
            except Exception as e:
                print(f"第{i}行解析出错 {line} ")
                raise e
    
    # def test_config(self):
    #     print(self.handle.get_network_states_block())
                
if __name__ == '__main__':
    unittest.main()