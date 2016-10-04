"""
This module facilitate connection with the switch through SSH.
"""

import logging
import os
import paramiko

class SSHCredential:
    """
    SSHCredential defines the connection details of a SSH channel.
    """
    config_path = ''
    config = None

    def __init__(self, host, port=22, username=None, password=None):
        # Load local SSH config files if not loaded.
        if not self.config_path:
            self._find_ssh_config()
            self._load_ssh_config()

        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @staticmethod
    def _find_ssh_config():
        p = os.path.expanduser('~/.ssh/config')
        if not os.path.exists(p):
            p = 'invalid'
        SSHCredential.config_path = p

    @staticmethod
    def _load_ssh_config():
        if SSHCredential.config_path == 'invalid':
            return

        # Instantiate the SSHConfig object.
        SSHCredential.config = paramiko.SSHConfig()
        # Load the file.
        with open(SSHCredential.config_path) as f:
            SSHCredential.config.parse(f)

class SSH(object):
    def __init__(self):
        # Set the logger.
        self.logger = logging.getLogger('libswitch.comm.SSH')

        # Define the variables.
        self.transport_list = []
        self.channel = None

    def connect(self, dest_cred, via=None):
        self.transport_list = []

        # Last item in the via is the destination.
        via.append(dest_cred)

        # Hop through the sites.
        for v in via:
            addr = (v.host, v.port)
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
            self.logger.debug('Connected to %s@%s:%d', v.username, v.host, v.port)
            self.transport_list.append(t)

        self.dest = dest_cred

    def send(self, cmd):
        # Open a shell session.
        t = self.transport_list.pop()
        ch = t.open_session()

        # Execute the command and get the return status.
        ch.exec_command(cmd)
        ret = ch.recv_exit_status()

        self.channel = ch

        #TODO: Dirty hack.
        # Re-establish the transport.
        addr = (self.dest.host, self.dest.port)
        # Get the last transport.
        t0 = self.transport_list[-1]
        # Start the forwarding.
        ch = t0.open_channel('direct-tcpip', addr, ('127.0.0.1', 0))
        t = paramiko.Transport(ch)
        t.start_client()
        t.auth_password(self.dest.username, self.dest.password)
        self.transport_list.append(t)

        return ret

    def receive(self, batch_size=1024):
        buf = ''
        while self.channel.recv_ready():
            buf += self._decode_byte_stream(self.channel.recv(batch_size))
        return buf

    @staticmethod
    def _decode_byte_stream(b):
        return b.decode('utf-8', errors='ignore')

    def __exit__(self, e_type, e_val, trace) :
        print('shit')
