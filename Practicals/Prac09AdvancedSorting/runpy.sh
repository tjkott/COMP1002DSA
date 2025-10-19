#!/bin/sh

#
# Script for St152 pracs S2/2004. Produces gnuplot output.
# Controlled by editing the sorts and max variables.
#
# Example Usage: 
#       ./run.sh > output.log ; gnuplot -persist output.log
#
# Author: Andrew Turpin (andrew@cs.curtin.edu.au)
# Date:    August 2004
# Modified: Patrick Peursum
# Date:    September 2009
#


# The "sorts" variable contains a list of sort-array pairs that are passed
# to TestHarness
# First char: sort type
# - i = insertion sort
# - b = bubble sort
# - s = selection sort
# - m = mergesort
# - q = quicksort (left-most pivot)
# - t = quicksort (median-of-three pivot)
# - y = quicksort (random pivot)
#
# Second char: initial order of array
# - a = ascending order
# - d = descending order
# - r = randomly ordered (actually: randomly swapped around)
# - n = ascending with 10% randomly swapped (ie: nearly sorted)
#
# Note: You will need to modify SortsTestHarness.py to recognise 'm', 't', and 'y'
# and call the respective sorting functions.
#
sorts="br sr mr qr tr yr bd sd md qd td yd bn sn mn qn tn yn ba sa ma qa ta ya"

# The "max" variable contains the maximum n that is passed to SortsTestHarness
max=8192


########################### DO NOT CHANGE BELOW THIS LINE ##################

tempFile="/tmp/st152$$"

function runEm()
    {
    for i in `awk 'BEGIN{for(i=1;i<='"$max"';i*=2)print i;exit}'`
    do
        python3 SortsTestHarness.py $i $sorts
    done
    }


#runEm | sort +0 -1 +1n -2 > $tempFile
runEm > $tempFile

# PP: Following line is a fix for MacOSX sh not understanding the -n flag
# Unfortunately, it is incompatible with Linux
# Perhaps a proper solution is to do the full path /bin/echo ?
#echo "plot\c"
echo -n "plot"
echo $sorts | awk '{for(i=1;i<NF;i++)printf"\"-\" using 2:3 t \"%s\" w lp,",$i}'
echo $sorts | awk '{i=NF;            printf"\"-\" using 2:3 t \"%s\" w lp",$i}'
echo ""

for s in $sorts 
do
    grep "$s" $tempFile
    echo "e"
done

rm $tempFile
