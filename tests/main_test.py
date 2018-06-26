import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from libswitch.comm import SSH as Comm
from secret import vias, targets

from libswitch.commands import Cisco

import logging
logger = logging.getLogger('libswitch.tests')

for target in targets:
	print(' >> {}'.format(target.host))
	
	c = Comm()
	c.connect(target, via=vias)

	s = 'copy run start'
	c.send(s);

	res = c.receive()
	with open(target.host, 'w') as f:
		f.write(res)
