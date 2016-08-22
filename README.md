# Nuke My LUKS
A simple network-based panic button designed to overwrite the LUKS header
with random data and reboot the computer in case of an emergency situation.

This tool can be useful for activists, human right workers and others that
face an adversary, such as law enforcement, that can force the subject to
disclose the encryption passwords for the computer's hard drives.

**IMPORTANT**: This will make **impossible** to recover any data stored in the disk even if the password is known. It is recommended to store your backups
encrypted and in a safe location. **Use this code with precaution.**

## How it works

Nuke My LUKS is divided in three different small pieces of code:
- client.py
- server.py
- generateconfig.py

In a nutshell, it works by sending a UDP broadcast message to port 1337 with a tag appended with a user-defined password. In case the password matches, the script for destroying the LUKS header is executed.

**NOTE:** Configure your firewall rules to allow UDP broadcast messages from your trusted computer running the client of Nuke My LUKS.

**PS:** Notice that it is possible to repurpose this code to use any shell script and perform other actions, but the original design is to destroy the LUKS header of the computer.

## Usage

1. Generate a config file using generateconfig.py:

```
julio@trouble:~/programming/Python/security/nukemyluks$ ./generateconfig.py mysupersecretpassword
[+] Configuration file created successfully.
```

2. Copy the generated config.ini file, server.py and the LUKS header destruction script to the computers you want to have this code running:
```
julio@trouble:~/programming/Python/security/nukemyluks$ cat config.ini
[config]
password_hash = $2a$13$fFEVaVHalvesYhVMUJTrUOjGPdUUvxzLIJUIqU8.jc3PJFbbQ.vSe
```
3. Run server.py and leave it running on the background

4. In case of panic, pass your password to client.py:
```
julio@trouble:~/programming/Python/security/nukemyluks$ ./client.py mysupersecretpassword
```

## Author
- [Julio Cesar Fort](http://www.whatever.io)
- Twitter: [@juliocesarfort](https://www.twitter.com/juliocesarfort)

## Credits
This code was inspired in the idea of [panicbcast](https://github.com/qnrq/panic_bcast) by [Niklas Femerstrand](http://www.qnrq.se/).
