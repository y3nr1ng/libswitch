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
        self.via_transport = []
        self.dest_cred = None
        self.channel = None

    def connect(self, dest_cred, via=None):
        if self.via_transport:
            self.logger.warning("Original transport list will be wiped")
            self.via_transport = []

        self.dest_cred = dest_cred

        # Hop through the sites.
        for v in via:
            addr = (v.host, v.port)
            if not self.via_transport:
                t = paramiko.Transport(addr)
            else:
                # Get the last transport.
                t0 = self.via_transport[-1]
                # Start the forwarding.
                ch = t0.open_channel('direct-tcpip', addr, ('127.0.0.1', 0))
                t = paramiko.Transport(ch)
            t.start_client()
            t.auth_password(v.username, v.password)
            self.logger.debug('Connected to %s@%s:%d', v.username, v.host, v.port)
            self.via_transport.append(t)

    def send(self, cmd):
        ch = self._connect_dest()

        # Execute the command and get the return status.
        ch.exec_command(cmd)
        ret = ch.recv_exit_status()

        self.channel = ch

        return ret

    def _connect_dest(self):
        cred = self.dest_cred

        addr = (cred.host, cred.port)
        # Get the last endpoint.
        t_end = self.via_transport[-1]
        # Start the forwarding.
        ch = t_end.open_channel('direct-tcpip', addr, ('127.0.0.1', 0))
        t = paramiko.Transport(ch)

        # Establish connection to the destination.
        t.start_client()
        t.auth_password(cred.username, cred.password)

        # Open a channel.
        return t.open_session()

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
