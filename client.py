#!/usr/bin/python
# Nuke My LUKS - client
# A simple network-based panic button designed to overwrite the LUKS header
# with random data and reboot the computer in case of an emergency situation.
# 
# IMPORTANT: This will make *impossible* to recover any data stored in the disk
# even if the password is known. Use this code with precaution.
#
# by Julio Cesar Fort - julio@whatever.io

import sys
import socket
import base64

ERROR = -1
DEFAULT_PORT = 1337

def main():
    if len(sys.argv) < 2:
        usage()
    
    secret = base64.b64encode(sys.argv[1])
    send_packet(secret)


def send_packet(secret):
    try:
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.bind(('', 0))
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except Exception as err:
        print "[!] Error creating broadcast socket: %s" % err
        sys.exit(ERROR)
    
    data = "nukemyluks_" + secret
    try:
        broadcast_socket.sendto(data, ('<broadcast>', DEFAULT_PORT))
        
    except Exception as err:
        print "[!] Error sending packet: %s" % err
        sys.exit(ERROR)


def usage():
    print "Usage: %s <password>" % sys.argv[0]
    sys.exit(0)


if __name__ == '__main__':
    main()