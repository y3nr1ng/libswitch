"""
This module facilitate connection with the switch through SSH.
"""

import os
import paramiko
import logging

class SSHCredential:
    def __init__(self, host, port=22, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

class SSH(object):
    def __init__(self):
        # Set the logger.
        self.logger = logging.getLogger('libswitch.comm.SSH')

    def connect(self, cred, via=[]):
        self.transport_list = []

        # Last item in the via is the destination.
        via.append(cred)

        # Hop through the sites.
        for v in via:
            addr = (v.host, v.port)
            self.logger.debug('Connect to {}:{}'.format(*addr))
            if not self.transport_list:
                t = paramiko.Transport(addr)
            else:
                # Get the last transport.
                t0 = self.transport_list[-1]
                # Start the forwarding.
                ch = t0.open_channel('direct-tcpip', addr, ('127.0.0.1', 0))
                t = paramiko.Transport(ch)
            t.start_client()
            t.auth_password(v.username, v.password)
            self.transport_list.append(t)

        # Open the session.
        t = self.transport_list[-1]
        self.session = t.open_session()

    def send(self, cmd):
        self.session.exec_command(cmd)
        ret = self.session.recv_exit_status()
        return ret

    def receive(self, batch_size=1024):
        buf = ''
        while self.session.recv_ready():
            buf += self._decode_byte_stream(self.session.recv(batch_size))
        return buf

    def _decode_byte_stream(self, b):
        return b.decode('utf-8', errors='ignore')

    def __exit__(self, e_type, e_val, trace) :
        print('shit')
