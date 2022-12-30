#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# GB Multi Rom Creator
# by S-I-M-O-N
# https://github.com/S-I-M-O-N/gb-multirom-creator
#
#
#
# Python script to build Gameboy multirom images based on Reiner Ziegler's startup.gb v1.3 provided as part of his readplus software.
# https://github.com/gb-archive/reinerziegler/blob/master/download/readplus_3327.tar.bz2
# The source code startup.asm is also available:
# https://github.com/gb-archive/reinerziegler/blob/master/download/startup.asm
#
# startup.gb is a menu for flash memory Gameboy carts. It was designed for the AM29F0XX based flash carts with original MBCs. 
#
# The menu provides the bootstrap for contained tools as well as up to 3 game roms.
# The menu and tools reside in the first 512kb of the rom.
# At the beginning of every following 512kb chunk of the memory it will check for available game roms. 
#
# Accordingly the memory map will be
# 0kb    -  512kb Menu & tools
# 513kb  - 1024kb ROM#1
# 1025kb - 1536kb ROM#2
# 1537kb - 2048kb ROM#3
# 
# As the game roms are not always 512kb the space is padded with zeros to complete 512kb, before the next rom is merged into the image.
#
# Roms (*.gb) need to be placed in the script folder.
#

import os
from sys import platform

if platform == "linux" or platform == "linux2" or platform == "darwin":
    # linux and mac os
    clear = lambda: os.system('clear')
elif platform == "win32":
    # windows
    clear = lambda: os.system('cls')

rom1=""
rom2=""
rom3=""
blank=os.path.join("res","blank.gb")
startup=os.path.join("res","startup.gb")

programversion="GB Multi Rom Creator v1.0"


def select_rom_1():
    print("Available roms:")
    i=1
    while True:
        while i < len(roms)+1:
            print(i,":",roms[i-1])
            i += 1
        print( "Please select rom #1. Enter 0 for blank.")
        item=int(input())
        global rom1
        if(item==0):
            rom1=blank
            break
        elif(item<=len(roms)+1):
            rom1=roms[item-1]
            if(os.path.getsize(rom1)>1*512*1024):
                print("The rom is larger than 512kb and thus not compatible. Please reselect.")
            else:
                break
        else:
            print( "Wrong selection: Select any number from 1-",len(roms))

def select_rom_2():
    print("Available roms:")
    i=1
    while True:
        while i < len(roms)+1:
            print(i,":",roms[i-1])
            i += 1
        print( "Please select rom #1. Enter 0 for blank.")
        item=int(input())
        global rom2
        if(item==0):
            rom2=blank
            break
        elif(item<=len(roms)+1):
            rom2=roms[item-1]
            if(os.path.getsize(rom2)>1*512*1024):
                print("The rom is larger than 512kb and thus not compatible. Please reselect.")
            else:
                break
        else:
            print( "Wrong selection: Select any number from 1-",len(roms))

def select_rom_3():
    print("Available roms:")
    i=1
    while True:
        while i < len(roms)+1:
            print(i,":",roms[i-1])
            i += 1
        print( "Please select rom #1. Enter 0 for blank.")
        item=int(input())
        global rom3
        if(item==0):
            rom3=blank
            break
        elif(item<=len(roms)+1):
            rom3=roms[item-1]
            if(os.path.getsize(rom3)>1*512*1024):
                print("The rom is larger than 512kb and thus not compatible. Please reselect.")
            else:
                break
        else:
            print( "Wrong selection: Select any number from 1-",len(roms))

roms=[]
for x in os.listdir():
    if x.endswith(".gb"):
        roms.append(x)

confirmation="n"

while confirmation != "y": 
    clear()
    print(programversion)
    print("")
    print("1:[ROM#1]")
    print("2:[ROM#2]")
    print("3:[ROM#3]")
    print("")
    select_rom_1()
    clear()
    print(programversion)
    print("")
    print("1:[",rom1,"]")
    print("2:[ROM#2]")
    print("3:[ROM#3]")
    print("")
    select_rom_2()
    clear()
    print(programversion)
    print("")
    print("1:[",rom1,"]")
    print("2:[",rom2,"]")
    print("3:[ROM#3]")
    print("")
    select_rom_3()
    clear()
    print(programversion)
    print("")
    print("1:[",rom1,"]")
    print("2:[",rom2,"]")
    print("3:[",rom3,"]")
    print("")
    print("Composition ok? (y/n)")
    confirmation=input()
   
    fo=open("multirom.gb", 'w')
    fo.close()
    fo=open("multirom.gb", 'ab')
    numBytes=0

    romsize=(os.path.getsize(startup))
    fi=open(startup, 'rb')
    while (numBytes<romsize):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    while (numBytes<1*512*1024):
        fo.write(b"\00")
        numBytes=numBytes+1
    fi.close()

    romsize=(os.path.getsize(rom1))
    fi=open(rom1, 'rb')
    while (numBytes<romsize+1*512*1024):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    while (numBytes<2*512*1024):
        fo.write(b"\00")
        numBytes=numBytes+1
    fi.close()

    romsize=(os.path.getsize(rom2))
    fi=open(rom2, 'rb')
    while (numBytes<romsize+2*512*1024):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    while (numBytes<3*512*1024):
        fo.write(b"\00")
        numBytes=numBytes+1
    fi.close()

    romsize=(os.path.getsize(rom3))
    fi=open(rom3, 'rb')
    while (numBytes<romsize+3*512*1024):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    while (numBytes<4*512*1024):
        fo.write(b"\00")
        numBytes=numBytes+1
    fi.close()

    fo.close()

    print("multirom.gb created")
