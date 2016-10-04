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
c.send('sh ver | i uptime|''IOS Software''|''Boot Loader''')
res = c.receive()
logger.info(res)

c.send('sh ip int')
res = c.receive()
logger.info(res)
