import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import libswitch.comm.SSH as Comm
from secret import vias, target

c = Comm()
c.connect(target, via=vias)
