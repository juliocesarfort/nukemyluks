#!/usr/bin/python
# Nuke My LUKS - server
# A simple network-based panic button designed to overwrite the LUKS header
# with random data and reboot the computer in case of an emergency situation.
# 
# IMPORTANT: This will make *impossible* to recover any data stored in the disk
# even if the password is known. Use this code with precaution.
#
# by Julio Cesar Fort - julio@whatever.io


import sys
import socket
import select
import os.path
import platform
import base64
import ConfigParser
from subprocess import Popen, PIPE

try:
    from bcrypt import hashpw, gensalt
except ImportError as err:
    print "[!] Error importing 'bcrypt': %s" % err
    sys.exit()

DEFAULT_PORT = 1337
ERROR = -1
NUKEMYLUK_CMD = './nukemyluks.sh'

def main():
    # check if we're running this code on Linux or not
    if 'Linux' not in platform.system():
        print "[!] Error: this can only run on Linux."
        sys.exit(ERROR)
    
    # create a broadcast UDP receving socket
    receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiving_socket.bind(('<broadcast>', DEFAULT_PORT))
    receiving_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    receiving_socket.setblocking(0)
    
    while True:
        result = select.select([receiving_socket], [], [])
        msg = result[0][0].recv(1024)
        
        if msg.startswith("nukemyluks_"):            
            try:
                configparser = ConfigParser.ConfigParser()
                configparser.read('config.ini')
                hashed_secret = configparser.get('config', 'password_hash')
            except Exception as err:
                print "[!] Error reading config file: %s" % err
                # TODO: send error message back containing the server IP
                sys.exit()
            
            secret = base64.b64decode(msg[len("nukemyluks_"):])
            
            if hashed_secret == hashpw(secret, hashed_secret):
                if not os.path.isfile(NUKEMYLUK_CMD):
                    print "[!] Cannot execute the %s (No such file)" % NUKEMYLUK_CMD
                    sys.exit(ERROR)

                cmd_output = Popen([NUKEMYLUK_CMD], stdout=PIPE,
                                   stdin=PIPE, stderr=PIPE)
                STDOUT, STDERR = cmd_output.communicate()
                print STDOUT
                # TODO: send a success message back containing the server IP

if __name__ == '__main__':
    main()
