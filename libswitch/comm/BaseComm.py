from abc import ABCMeta, abstractmethod

class BaseComm(metaclass=ABCMeta):
    @abstractmethod
    def connect(self, dest_cred, via=None):
        pass

    @abstractmethod
    def send(self, cmd):
        pass

    @abstractmethod
    def receive(self, batch_size=1024):
        pass

    @abstractmethod
    def close(self):
        pass
