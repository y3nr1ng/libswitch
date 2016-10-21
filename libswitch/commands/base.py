"""
Common definitinos for the high-level instructions.
"""

from abc import ABCMeta, abstractmethod

class Base(metaclass=ABCMeta):
    @abstractmethod
    def setComm(self, comm):
        pass

    @abstractmethod
    def listChannel(self):
        pass
