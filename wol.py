#!/usr/bin/env python3
#
# Based on wol.py from http://code.activestate.com/recipes/358449-wake-on-lan/
# Amended to use configuration file and hostnames
#
# Copyright (C) Fadly Tabrani, B Tasker
#
# Released under the PSF License See http://docs.python.org/2/license.html
#
#


import socket
import struct
import configparser
import re

myconfig = {}

class WakeOnLan:
        def __init__(self, host, mydir):
                self.host = host
                self.mydir = mydir

        def wake(self):
                """ Switches on remote computers using WOL. """
                global myconfig

                try:
                        macaddress = myconfig[self.host]['mac']

                except:
                        return False

                # Check mac address format
                found = re.fullmatch('^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([\s][A-F0-9]{2}){5})|([a-f0-9]{2}(([:][a-f0-9]{2}){5}|([-][a-f0-9]{2}){5}|([\s][a-f0-9]{2}){5}))$', macaddress)
                #We must found 1 match , or the MAC is invalid
                if found:
	        #If the match is found, remove mac separator [:-\s]
                        macaddress = macaddress.replace(macaddress[2], '')
                else:
                        raise ValueError('Incorrect MAC address format')
	
                # Pad the synchronization stream.
                data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
                send_data = b''

                # Split up the hex values and pack.
                for i in range(0, len(data), 2):
                        send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])

                # Broadcast it to the LAN.
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(send_data, (myconfig['General']['broadcast'], 7))
                return True


        def loadConfig(self):
	        """ Read in the Configuration file to get CDN specific settings"""
	        global myconfig
	        Config = configparser.ConfigParser()
	        Config.read(self.mydir+"/wol_config.ini")
	        sections = Config.sections()
	        dict1 = {}
	        for section in sections:
		        options = Config.options(section)

		        sectkey = section
		        myconfig[sectkey] = {}


		        for option in options:
			        myconfig[sectkey][option] = Config.get(section,option)


	        return myconfig # Useful for testing

# #if __name__ == '__main__':
#         mydir = os.path.dirname(os.path.abspath(__file__))
#         try: arg = sys.argv[1]
#         except: arg = 'myPC'
#         #except: arg = 'list'
#         wol = WakeOnLan(arg)
#         conf = wol.loadConfig()
#         try:
#                 # Use macaddresses with any separators.
#                 if arg == 'list':
#                         print('Configured Hosts:')
#                         for i in conf: 
#                                 if i != 'General': print('\t',i)
#                         print('\n')
#                 if arg == 'myPC':
#                         if not wol.wake_on_lan(): 
#                                 print('Invalid Hostname specified')
#                         else: 
#                                 print('Magic packet should be winging its way')
#                 else: print("test")
#         except:
#                 wol.usage()