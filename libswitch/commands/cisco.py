from .base import Base
from libswitch.device.channel import Types as AbstractChanType
import logging

ActualChanType = ['GigabitEthernet', 'Vlan', 'Port-channel']

class Cisco(Base):
    def __init__(self):
        # Set the logger.
        self.logger = logging.getLogger('libswitch.comm.cisco')

    def setComm(self, comm):
        self.comm = comm

    def listChannel(self):
        c = self.comm
        req = 'sh int sum | i ({})'.format('|'.join(list))
        c.send(req)
        res = c.receive()

        logger.info(res)
