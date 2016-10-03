import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import libswitch.comm.SSH as Comm
from secret import vias, target

import logging
logger = logging.getLogger('libswitch.tests')

c = Comm()
c.connect(target, via=vias)

#DEBUG
c.send('show clu mem')
res = c.receive()
logger.info(res)
