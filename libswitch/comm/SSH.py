"""
This module facilitate connection with the switch through SSH.
"""

import os
import paramiko

class SSH(object):
    def __init__(self, hops=None) :
        # Intermediate SSH hops.
        self.hops = hops

        # SSH client.
        self.handler = paramiko.SSHClient()

        # Setup the policies.
        self.handler.load_system_host_keys()
        self.handler.set_missing_host_key_policy(paramiko.WarningPolicy())

    def __load_ssh_config(self) :
        """
        Load user SSH config parameters.
        """

        self.ssh_config = paramiko.SSHConfig()

        # Load the configurations if exist.
        ssh_config_file = os.path.expanduser("~/.ssh/config")
        if os.path.exists(ssh_config_file) :
            with open(ssh_config_file) as f :
                self.ssh_config.parse(f)

        print('Dump the SSH config')
        print(self.ssh_config)

    def __enter__(self) :
        self.__load_ssh_config()
        return self

    def __establish(self) :
        """
        Establish the SSH connection.
        """

    def __connect(self, host, username=None, password=None) :
        """
        The actual function that establish the connection.
        """

        # Lookup in the config file.
        explicit_config = self.ssh_config.lookup(host)

        if 'hostname'
        if username is None :

        if password is None :


    def connect(self, host, username=None, password=None) :
        # Establish the connection with hops first.
        if hops :
            for h in hops :



    def __exit__(self, e_type, e_val, trace) :
