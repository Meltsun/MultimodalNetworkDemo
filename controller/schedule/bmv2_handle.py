from dataclasses import dataclass,field
import datetime
from typing import Tuple

@dataclass
class MultipathState:
    num:Tuple[int,int,int]
    order:Tuple[int,int,int]
    time:datetime.datetime=field(default_factory=datetime.datetime.now)

def download_multipath_state(multipath:MultipathState)->None:
    #TODO
    pass