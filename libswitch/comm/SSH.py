"""
This module facilitate connection with the switch through SSH.
"""

import os
import paramiko
import logging

class SSHCredential:
    def __init__(self, hostname, username=None, password=None):


class SSH(object):
    def __init__(self):
        # Set the logger.
        self.logger = logging.getLogger('libswitch.comm.SSH')

    def __enter__(self):
        self.__load_ssh_config()
        return self

    def connect(self, hostname, username=None, password=None):


    def __exit__(self, e_type, e_val, trace) :
