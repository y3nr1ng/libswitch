import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import libswitch.comm.SSH as Comm
from secret import vias, target

import logging
logger = logging.getLogger('libswitch.tests')
import time

c = Comm()
c.connect(target, via=vias)

#DEBUG
c.send('sh ver')
res = c.receive()
logger.info(res)

c.send('sh clu mem')
res = c.receive()
logger.info(res)

c.send('sh proc cpu hist')
res = c.receive()
logger.info(res)

c.send('sh proc cpu sorted 5s')
res = c.receive()
logger.info(res)
