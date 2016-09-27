"""
This module facilitate connection with the switch through SSH.
"""

import os
import paramiko
import logging

class SSH(object):
    def __init__(self, hops=None) :
        # Set the logger.
        self.logger = logging.getLogger('libswitch.comm.SSH')

        # Intermediate SSH hops.
        self.hops = hops

        # SSH client.
        self.handler = paramiko.SSHClient()

        # Setup the policies.
        self.handler.load_system_host_keys()
        self.handler.set_missing_host_key_policy(paramiko.WarningPolicy())

    def __enter__(self) :
        self.__load_ssh_config()
        return self

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

    def __connect(self, hostname, username=None, password=None) :
        """
        The actual function that establish the connection.
        """

        # Lookup in the config file.
        explicit_config = self.ssh_config.lookup(host)

        # Override the hostname.
        if 'hostname' in explicit_config :
            config['hostname'] = explicit_config['hostname']
        else :
            config['hostname'] = hostname

        # Override the username if not assigned.
        if username is None :
            if 'username' in explicit_config :
                config['username'] = explicit_config['username']
            else :
                self.logger.error('Username not provided')
        else :
            config['username'] = username

        # Override the password if not assigned.
        if password is None :
            # Use the identity file first.
            if 'identityfile' in explicit_config :
                config['key_filename'] = explicit_config['identityfile']
            elif 'password' in explicit_config :
                config['password'] = explicit_config['password']
            else :
                self.logger.error('Nor keyfile or password is provided')
        else :
            config['password'] = password

        # Override the port.
        if 'port' in explicit_config :
            config['port']  = explicit_config['port']

        # Override the proxy.
        if 'proxycommand' in explicit_config :
            config['sock'] = paramiko.ProxyCommand(explicit_config['proxycommand'])

        # Establish the connection.
        try :
            self.handler.connect(config)
        except paramiko.AuthenticationException :
            self.logger.error('Authentication failed')
        except Exception as e :
            self.logger.error(str(e))

    def connect(self, hostname, username=None, password=None) :
        # Establish the connection with hops first.
        if self.hops :
            self.logger.error('Hop through servers not supported')

    def __exit__(self, e_type, e_val, trace) :
        print('dummy')
