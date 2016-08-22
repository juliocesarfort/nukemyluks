#!/usr/bin/python
# Nuke My LUKS - configuration generator
# A simple network-based panic button designed to overwrite the LUKS header
# with random data and reboot the computer in case of an emergency situation.
# 
# IMPORTANT: This will make *impossible* to recover any data stored in the disk
# even if the password is known. Use this code with precaution.
#
# by Julio Cesar Fort, Wildfire Labs /// Blaze Information Security
#
# Copyright 2016, Blaze Information Security
# https://www.blazeinfosec.com

import sys
import ConfigParser
try:
    from bcrypt import hashpw, gensalt
except ImportError:
    print "[!] Error importing 'bcrypt': %s" % err
    sys.exit()

DEFAULT_ROUNDS = 13

def main():
    if len(sys.argv) < 2:
        usage()

    hashed_password = hashpw(sys.argv[1], gensalt(log_rounds=DEFAULT_ROUNDS))

    configparser = ConfigParser.ConfigParser()
    configparser.add_section('config')
    configparser.set('config', 'password_hash', hashed_password)
    
    try:
        config_file = open('config.ini', 'w')
        configparser.write(config_file)
    except Exception as err:
        print "[!] Error creating config file: %s" % err
        sys.exit()
        
    print "[+] Configuration file created successfully."
    config_file.close()
    
   
def usage():
    print "Usage: %s <password>" % sys.argv[0]
    sys.exit(0)
    

if __name__ == '__main__':
    main()