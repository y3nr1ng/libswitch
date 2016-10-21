import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from libswitch.comm import SSH as Comm
from secret import vias, target

from libswitch.commands import Cisco

import logging
logger = logging.getLogger('libswitch.tests')

c = Comm()
c.connect(target, via=vias)

##DEBUG
#c.send('sh ver | i uptime|''IOS Software''|''Boot Loader''')
#res = c.receive()
#logger.info(res)

cmd = Cisco()
cmd.setComm(c)
c.listChannel()
