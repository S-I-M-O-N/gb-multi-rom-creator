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
# Version 2 of the script features a new approach to a multirom menu currently under developed by b0h.
# https://github.com/b0h5stuff/startup.gb
#
# The new concept uses a dedicated bank where the roms are temporarily flashed to for running.
# This allows to add more than 3 roms to one cartridge.
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
romno=1
romsselectedsize=0
chipsize=2048
maxromsize=256
startupsize=32
blank=os.path.join("res","blank.gb")
startup=os.path.join("res","startup22.gb")
mode=2
programversion="GB Multi Rom Creator v2.0"

def select_mode():
    global chipsize
    global startup
    global maxromsize
    global startupsize
    global mode
    while True:
        clear()
        print(programversion)
        print("Startup Menu:",startup)
        print("Chip size:",chipsize,"kB")
        print("Max rom size:",maxromsize,"kB")
        print()
        print("1: Select startup menu")
        print()
        print( "Please select menu entry. Enter 0 to exit menu.")
        item=int(input())
        if(item==0):
            print()
        elif(item==1):
            clear()
            print("1: startup.gb (v1.3: Max 3 roms for AM29F016)")
            print("2: startup22.gb (v2.2: Multiple roms with temporary flashing)")
            print()
            print( "Please select menu entry. Enter 0 to exit menu.")
            item2=int(input())
            if(item2==0):
               print() 
            elif(item2==1):
                startup=os.path.join("res","startup.gb")
                startupsize=os.path.getsize(startup)/1024
                mode=1
                maxromsize=512
            elif(item2==2):
                startup=os.path.join("res","startup22.gb")
                startupsize=os.path.getsize(startup)/1024
                mode=2
            else:
                print( "Wrong selection: Select any number from 0-2")
        else:
            print( "Wrong selection: Select any number from 0-2")
        if mode==1:
            break
        clear()
        print(programversion)
        print("Startup Menu:",startup)
        print("Chip size:",chipsize,"kB")
        print("Max rom size:",maxromsize,"kB")
        print()
        print("1: Select flash chip")
        print()
        print( "Please select menu entry. Enter 0 to exit menu.")
        item=int(input())
        if(item==0):
            break
        elif(item==1):
            clear()
            print("1: 2048kB (AM29F016, etc.)")
            print("2: 1024kB (AM29F080, etc.)")
            print("3:  512kB (AM29F040, etc.)")
            print()
            print( "Please select menu entry. Enter 0 to exit menu.")
            item2=int(input())
            if(item2==0):
                break
            elif(item2==1):
                chipsize=2048
                maxromsize=256
                if mode==1:
                    maxromsize=512
                break
            elif(item2==2):
                chipsize=1024
                maxromsize=128
                break
            elif(item2==3):
                chipsize=512
                maxromsize=64
                break
            else:
                print( "Wrong selection: Select any number from 0-3")
                break


def select_rom():
    global romno
    global confirmation
    global romsselected
    global romsselectedsize
    global maxromsize
    global chipsize
    global startupsize
    print("Available roms:")
    i=1
    while True:
        while i < len(roms)+1:
            print(i,":",roms[i-1],"[",int(os.path.getsize(roms[i-1])/1024),"kB ]")
            i += 1
        print( "Please select rom",romno,"Enter 0 to stop adding roms.")
        item=int(input())
        if(item==0):
            confirmation = "y"
            break
        elif(item<=len(roms)+1):
            if(os.path.getsize(roms[item-1])>maxromsize*1024):
                print("The rom is larger than",maxromsize,"kB and thus not compatible. Please reselect.")
            elif(os.path.getsize(roms[item-1])>(chipsize-startupsize-maxromsize-(romsselectedsize/1024))*1024):
                print("The rom is larger than the remaining free space. Please reselect.")
            else:
                romsselected.append(roms[item-1])
                romsselectedsize=romsselectedsize+os.path.getsize(roms[item-1])
                romno += 1
                break
        else:
            print( "Wrong selection: Select any number from 1-",len(roms))


roms=[]
for x in os.listdir():
    if x.endswith(".gb"):
        roms.append(x)

confirmation="n"

clear()
select_mode()

romsselected=[startup]
confirmation = "n"
while confirmation != "y": 
    i=1
    clear()
    print(programversion)
    print("Startup Menu:",startup)
    print("Chip size:",chipsize,"kB")
    print("Max rom size:",maxromsize,"kB")
    if mode==2:
        print("Size menu and selected roms:",int(startupsize+(romsselectedsize/1024)),"kB")
        print("Remaining space for additional roms:",int(chipsize-startupsize-maxromsize-(romsselectedsize/1024)),"kB")
        print("Temp r/w memory between",chipsize/4,"kB and",chipsize/4+maxromsize,"kB") 
    print("")
    print("Selected roms:")
    while i < len(romsselected):
        print(i,":",romsselected[i])
        i += 1
    print("")
    select_rom()
    i=1
    clear()
    print(programversion)
    print("Startup Menu:",startup)
    print("Chip size:",chipsize,"kB")
    print("Max rom size:",maxromsize,"kB")
    print("")
    print("Selected roms:")
    while i < len(romsselected):
        print(i,":",romsselected[i])
        i += 1
    print("")
    if mode==1:
        if i==4:
            break
            
  
romno=0
romsselectedsize=0
fo=open("multirom.gb", 'w')
fo.close()
fo=open("multirom.gb", 'ab')

while romno < len(romsselected):
    numBytes=0

    romsize=(os.path.getsize(romsselected[romno]))
    if mode==2:
        if int(romsselectedsize)<int(chipsize*1024/4):
            if int(romsize)>(int(chipsize*1024/4))-int(romsselectedsize):
                pad=int(chipsize*1024/4)-int(romsselectedsize)
                while (numBytes<pad+(maxromsize*1024)):
                    fo.write(b"\00")
                    numBytes=numBytes+1
                numBytes=0
                
    fi=open(romsselected[romno], 'rb')
    while (numBytes<romsize):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    if mode==1:
        while (numBytes<maxromsize*1024):
            fo.write(b"\00")
            numBytes=numBytes+1
    fi.close()
    fo.close()
    romsselectedsize=os.path.getsize("multirom.gb")
    fo=open("multirom.gb", 'ab')
    romno += 1

fo.close()
numBytes=os.path.getsize("multirom.gb")
fo=open("multirom.gb", 'ab')
while (numBytes<(chipsize*1024)):
    fo.write(b"\00")
    numBytes=numBytes+1

fo.close()

print("multirom.gb created")
