import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import libswitch.comm.SSH

c = libswitch.comm.SSH(hops=hops)
c.connect(sw_host, username=sw_user, password=sw_pass)
