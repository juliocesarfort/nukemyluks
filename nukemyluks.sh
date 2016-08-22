#!/bin/sh
# Nuke My LUKS
# Following what ArchLinux says about it, overwrite the first 10MB:
# https://wiki.archlinux.org/index.php/Dm-crypt/Drive_preparation

DISK=$(sudo /sbin/blkid | /bin/grep crypto_LUKS | /usr/bin/cut -d ":" -f 1)
echo $DISK
/bin/dd if=/dev/urandom of=$DISK bs=512 count=20480
/sbin/shutdown -P now
