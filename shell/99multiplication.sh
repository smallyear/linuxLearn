#!/bin/sh

for i in {1..9};do
	for j in `seq 1 $i`;do
		let c=$i*$j ;echo -e "${i}x${j}=$c\t\c"
	done
	echo
done
