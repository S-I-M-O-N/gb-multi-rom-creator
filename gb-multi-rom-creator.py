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


romno=1
rom0no=1
rom1no=0
rom2no=0
rom3no=0
romsselectedsize=0
chipsize=2048
maxromsize=chipsize/4
erasesize=maxromsize/2
startupsize=32
cart0free=(chipsize/4)-startupsize
cart1free=(chipsize/4)-erasesize
cart2free=(chipsize/4)
cart3free=(chipsize/4)
blank=os.path.join("res","blank.gb")
startup=os.path.join("res","startup22.gb")
mode=2
programversion="GB Multi Rom Creator v2.1"

def select_mode():
    global chipsize
    global startup
    global maxromsize
    global startupsize
    global erasesize
    global cart0free
    global cart1free
    global cart2free
    global cart3free
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
                cart0free=0
                cart1free=maxromsize
                erasesize=0
                mode=1
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
            confirmation = "n"
            clear()
            while confirmation != "y":
                print("1: 2048kB (AM29F016, etc.)")
                print("2: 1024kB (AM29F080, etc.)")
                print("3:  512kB (AM29F040, etc.)")
                print()
                print( "Please select menu entry. Enter 0 to exit menu.")
                item2=int(input())
                if(item2==0):
                    confirmation = "y"
                elif(item2==1):
                    chipsize=2048
                    confirmation = "y"
                elif(item2==2):
                    chipsize=1024
                    confirmation = "y"
                elif(item2==3):
                    chipsize=512
                    confirmation = "y"
                else:
                    print( "Wrong selection: Select any number from 0-3")
                
                maxromsize=chipsize/4
                erasesize=maxromsize/2
                cart0free=maxromsize-startupsize
                if mode==1:
                    cart0free=0
                cart1free=maxromsize-erasesize
                if mode==1:
                    cart1free=maxromsize
                cart2free=maxromsize
                cart3free=maxromsize
            break


def select_rom():
    global romno
    global rom0no
    global rom1no
    global rom2no
    global rom3no
    global confirmation
    global romsselected0
    global romsselected1
    global romsselected2
    global romsselected3
    global romsselectedsize
    global maxromsize
    global chipsize
    global startupsize
    global erasesize
    global cart0free
    global cart1free
    global cart2free
    global cart3free
    
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
            elif(os.path.getsize(roms[item-1])<=cart0free*1024):
                romsselected0.append(roms[item-1])
                cart0free=cart0free-(os.path.getsize(roms[item-1])/1024)
                rom0no += 1
                romno += 1
                break
            elif(os.path.getsize(roms[item-1])<=cart1free*1024):
                romsselected1.append(roms[item-1])
                cart1free=cart1free-(os.path.getsize(roms[item-1])/1024)
                if mode==1:
                    cart1free=0
                rom1no += 1
                romno += 1
                break
            elif(os.path.getsize(roms[item-1])<=cart2free*1024):
                romsselected2.append(roms[item-1])
                cart2free=cart2free-(os.path.getsize(roms[item-1])/1024)
                if mode==1:
                    cart2free=0
                rom2no += 1
                romno += 1
                break
            elif(os.path.getsize(roms[item-1])<=cart3free*1024):
                romsselected3.append(roms[item-1])
                cart3free=cart3free-(os.path.getsize(roms[item-1])/1024)
                if mode==1:
                    cart3free=0
                rom3no += 1
                romno += 1
                break
            else:
                print("The rom is larger than the remaining free space. Please reselect.")
        else:
            print( "Wrong selection: Select any number from 1-",len(roms))


roms=[]
for x in os.listdir():
    if x.endswith(".gb"):
        roms.append(x)

confirmation="n"

clear()
select_mode()

romsselected0=[startup]
romsselected1=[]
romsselected2=[]
romsselected3=[]
confirmation = "n"
while confirmation != "y": 
    i=1
    clear()
    print(programversion)
    print("Startup Menu:",startup)
    print("Chip size:",chipsize,"kB")
    print("Max rom size:",maxromsize,"kB")
    print("Remaining cart space for additional roms:") #,int(chipsize-startupsize-maxromsize-(romsselectedsize/1024)),"kB")
    print("#0[",int(cart0free),"kB ] ","#1[",int(cart1free),"kB ] ","#2[",int(cart2free),"kB ] ","#3[",int(cart3free),"kB ] ")
    print("")
    print("Selected roms:")
    while i < len(romsselected0):
        print(i,":",romsselected0[i])
        i += 1
    i=0
    while i < len(romsselected1):
        print(i+len(romsselected0),":",romsselected1[i])
        i += 1
    i=0
    while i < len(romsselected2):
        print(i+len(romsselected0)+len(romsselected1),":",romsselected2[i])
        i += 1
    i=0
    while i < len(romsselected3):
        print(i+len(romsselected0)+len(romsselected1)+len(romsselected2),":",romsselected3[i])
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
    while i < len(romsselected0):
        print(i,":",romsselected0[i])
        i += 1
    i=0
    while i < len(romsselected1):
        print(i+len(romsselected0),":",romsselected1[i])
        i += 1
    i=0
    while i < len(romsselected2):
        print(i+len(romsselected0)+len(romsselected1),":",romsselected2[i])
        i += 1
    i=0
    while i < len(romsselected3):
        print(i+len(romsselected0)+len(romsselected1)+len(romsselected2),":",romsselected3[i])
        i += 1
    print("")
    if mode==1:
        if i==4:
            break
            
  
rom0no=0
rom1no=0
rom2no=0
rom3no=0
romsselectedsize=0
fo=open("multirom.gb", 'w')
fo.close()
fo=open("multirom.gb", 'ab')

while rom0no < len(romsselected0):
    numBytes=0

    romsize=(os.path.getsize(romsselected0[rom0no]))
                
    fi=open(romsselected0[rom0no], 'rb')
    while (numBytes<romsize):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    if mode==1:
        while (numBytes<maxromsize*1024):
            fo.write(b"\00")
            numBytes=numBytes+1
    fi.close()
    rom0no += 1

numBytes=int(maxromsize-cart0free)*1024
while (numBytes<(maxromsize+erasesize)*1024):
    fo.write(b"\00")
    numBytes=numBytes+1

while rom1no < len(romsselected1):
    numBytes=0

    romsize=(os.path.getsize(romsselected1[rom1no]))
                
    fi=open(romsselected1[rom1no], 'rb')
    while (numBytes<romsize):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    if mode==1:
        while (numBytes<(maxromsize)*1024):
            fo.write(b"\00")
            numBytes=numBytes+1
    fi.close()
    rom1no += 1

numBytes=int(maxromsize-cart1free)*1024
while (numBytes<maxromsize*1024):
    fo.write(b"\00")
    numBytes=numBytes+1

while rom2no < len(romsselected2):
    numBytes=0

    romsize=(os.path.getsize(romsselected2[rom2no]))
                
    fi=open(romsselected2[rom2no], 'rb')
    while (numBytes<romsize):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    if mode==1:
        while (numBytes<maxromsize*1024):
            fo.write(b"\00")
            numBytes=numBytes+1
    fi.close()
    rom2no += 1

numBytes=int(maxromsize-cart2free)*1024
while (numBytes<maxromsize*1024):
    fo.write(b"\00")
    numBytes=numBytes+1

while rom3no < len(romsselected3):
    numBytes=0

    romsize=(os.path.getsize(romsselected3[rom3no]))
                
    fi=open(romsselected3[rom3no], 'rb')
    while (numBytes<romsize):
        fo.write(fi.read(1))
        numBytes=numBytes+1
    if mode==1:
        while (numBytes<maxromsize*1024):
            fo.write(b"\00")
            numBytes=numBytes+1
    fi.close()
    rom3no += 1

numBytes=int(maxromsize-cart3free)*1024
while (numBytes<int(maxromsize*1024)):
    fo.write(b"\00")
    numBytes=numBytes+1

fo.close()

print("multirom.gb created")
