# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 13:55:11 2017

@author: simcha
"""

import _winreg
usb_devices=[]
index = 0
with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Enum\USB') as root_usb:
    while True:
        try:
            subkey = _winreg.EnumKey(root_usb, index)
            usb_devices.append(subkey)
            index += 1
        except WindowsError as e:
            if e[0] == 259: # No more data is available
                break
            elif e[0] == 234: # more data is available
                index += 1
                continue
            raise e
print('parse these', usb_devices)