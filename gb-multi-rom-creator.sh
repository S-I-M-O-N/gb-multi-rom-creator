#!/bin/bash
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
# https://github.com/S-I-M-O-N
#
#
#
# Shell script to build Gameboy multirom images based on Reiner Ziegler's startup.gb v1.3 provided as part of his readplus software.
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
#

programversion="GB Multi Rom Creator v1.0"

select_rom_1 ()
{
	echo "Please select rom #1. Enter 0 for blank."
	select item; do
		# Check the selected menu item number
		if [ 1 -le "$REPLY" ] && [ "$REPLY" -le $# ];

		then
			rom1=$item
			break;
		elif  (("$REPLY"==0 ));
		then	
			rom1="res/blank.gb"
			break;
		else
			echo "Wrong selection: Select any number from 1-$#"
		fi
	done
}

select_rom_2 ()
{

	echo "Please select rom #2. Enter 0 for blank."
	select item; do
		# Check the selected menu item number
		if [ 1 -le "$REPLY" ] && [ "$REPLY" -le $# ];

		then
			rom2=$item
			break;
		elif  (("$REPLY"==0 ));
		then	
			rom2="res/blank.gb"
			break;
		else
			echo "Wrong selection: Select any number from 1-$#"
		fi
	done
}

select_rom_3 ()
{

	echo "Please select rom #3. Enter 0 for blank"
	select item; do
		# Check the selected menu item number
		if [ 1 -le "$REPLY" ] && [ "$REPLY" -le $# ];

		then
			rom3=$item
			break;
		elif  (("$REPLY"==0 ));
		then	
			rom3="res/blank.gb"
			break;
		else
			echo "Wrong selection: Select any number from 1-$#"
		fi
	done
}


readarray -t roms < <(ls *.gb)

confirmation="n"

while [ "$confirmation" != "y" ]
do
	clear
	echo $programversion
	echo
	echo "1:[ROM#1]"
	echo "2:[ROM#2]"
	echo "3:[ROM#3]";echo 
	echo
	select_rom_1 "${roms[@]}"
	clear
	echo $programversion
	echo
	echo "1:[$rom1]"
	echo "2:[ROM#2]"
	echo "3:[ROM#3]";echo 
	echo
	select_rom_2 "${roms[@]}"
	clear
	echo $programversion
	echo
	echo "1:[$rom1]"
	echo "2:[$rom2]"
	echo "3:[ROM#3]";echo 
	echo
	select_rom_3 "${roms[@]}"
	clear
	echo $programversion
	echo
	echo "1:[$rom1]"
	echo "2:[$rom2]"
	echo "3:[$rom3]";echo 
	echo
	echo "Composition ok? (y/n)"
	read confirmation
done

	rom1_size=$(wc -c "$rom1" | cut -d ' ' -f 1)
	case $rom1_size in
		32768)
			#echo "32kb"
			cat "$rom1" > res/rom1.gb
			for i in {1..30..1}
			do
				cat res/blank.gb >> res/rom1.gb
			done
			;;
		65536)
			#echo "64kb"
			cat "$rom1" > res/rom1.gb
			for i in {1..28..1}
			do
				cat res/blank.gb >> res/rom1.gb
			done
			;;
		131072)
			#echo "128kb"
			cat "$rom1" > res/rom1.gb
			for i in {1..24..1}
			do
				cat res/blank.gb >> res/rom1.gb
			done
			;;
		262144)
			#echo "256kb"
			cat "$rom1" > res/rom1.gb
			for i in {1..16..1}
			do
				cat res/blank.gb >> res/rom1.gb
			done
			;;
		524288)
			#echo "512kb"
			cat "$rom1" > res/rom1.gb
			;;
		*)
			rom1_kb=$((rom1_size/1024));
			echo "$rom1 has a non standard size of $rom1_kb"
			;;
	esac

	rom2_size=$(wc -c "$rom2" | cut -d ' ' -f 1)
	case $rom2_size in
		32768)
			#echo "32kb"
			cat "$rom2" > res/rom2.gb
			for i in {1..30..1}
			do
				cat res/blank.gb >> res/rom2.gb
			done
			;;
		65536)
			#echo "64kb"
			cat "$rom2" > res/rom2.gb
			for i in {1..28..1}
			do
				cat res/blank.gb >> res/rom2.gb
			done
			;;
		131072)
			#echo "128kb"
			cat "$rom2" > res/rom2.gb
			for i in {1..24..1}
			do
				cat res/blank.gb >> res/rom2.gb
			done
			;;
		262144)
			#echo "256kb"
			cat "$rom2" > res/rom2.gb
			for i in {1..16..1}
			do
				cat res/blank.gb >> res/rom2.gb
			done
			;;
		524288)
			#echo "512kb"
			cat "$rom2" > res/rom2.gb
			;;
		*)
			rom2_kb=$((rom2_size/1024));
			echo "$rom2 has a non standard size of $rom1_kb"
			;;
	esac

	rom3_size=$(wc -c "$rom3" | cut -d ' ' -f 1)
	case $rom3_size in
		32768)
			#echo "32kb"
			cat "$rom3" > res/rom3.gb
			for i in {1..30..1}
			do
				cat res/blank.gb >> res/rom3.gb
			done
			;;
		65536)
			#echo "64kb"
			cat "$rom3" > res/rom3.gb
			for i in {1..28..1}
			do
				cat res/blank.gb >> res/rom3.gb
			done
			;;
		131072)
			#echo "128kb"
			cat "$rom3" > res/rom3.gb
			for i in {1..24..1}
			do
				cat res/blank.gb >> res/rom3.gb
			done
			;;
		262144)
			#echo "256kb"
			cat "$rom3" > res/rom3.gb
			for i in {1..16..1}
			do
				cat res/blank.gb >> res/rom3.gb
			done
			;;
		524288)
			#echo "512kb"
			cat "$rom3" > res/rom3.gb
			;;
		*)
			rom3_kb=$((rom3_size/1024));
			echo "$rom3 has a non standard size of $rom3_kb"
			;;
	esac

	cat res/startup.gb > res/rom0.gb
	for i in {1..28..1}
	do
		cat res/blank.gb >> res/rom0.gb
	done
cat res/rom0.gb res/rom1.gb res/rom2.gb res/rom3.gb > multirom.gb

echo "multirom.gb created"
