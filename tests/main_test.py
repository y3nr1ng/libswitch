import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import libswitch.comm.SSH as Comm
from secret import hops, sw_host, sw_user, sw_pass

c = Comm(hops=hops)
c.connect(sw_host, username=sw_user, password=sw_pass)
