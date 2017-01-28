#!/bin/bash

# requires: gnuplot, gnuplot-x11
# usage: ./draw.sh FILE [X_START X_END]

set -e
# set -o xtrace

#cd /caffe/visualization

if [ ! -f "$1" ]
then
    echo "File not found."
    exit
fi


LOSS_STEP=10
MAP_STEP=500
CLASS_NUM=1


if [ "$#" -ne 3 ]
then
    XRAN="[0:]"
else
    XRAN="[$2:$3]"
fi

cat "$1" | egrep "Train net output #0:" | egrep -o "mbox_loss = .*$" | cut -d ' ' -f 3 >nonsmloss.txt

cat "$1" | egrep -o ", loss = .*$" | cut -d ' ' -f 4 >smloss.txt

cat "$1" | egrep -o "Test net output \#0: detection_eval_m = .*$" | cut -d ' ' -f 7 >mAP.txt

for i in $(seq 1 $CLASS_NUM);
do
    cat "$1" | egrep -o "Test net output \#"$i": detection_eval_"$i" = .*$" | cut -d ' ' -f 7 >AP$i.txt
done

FIRSTITER=`cat "$1" | egrep -o "Iteration [0-9]*" | head -n 1 | cut -d ' ' -f 2`




GNUPLOT_CMD="set term png size 1024,768 enhanced; set output \"last.png\"; set xrange $XRAN; set yrange [0:]; set y2range [0:100]; set grid xtics lt 0; set grid ytics lt 0; set grid y2tics lt 0; set y2tics; set tics out; "
GNUPLOT_CMD="${GNUPLOT_CMD} plot \"nonsmloss.txt\" using (\$0*$LOSS_STEP+$FIRSTITER):1 axis x1y1 with lines title 'Loss', "
GNUPLOT_CMD="${GNUPLOT_CMD} \"smloss.txt\" using (\$0*$LOSS_STEP+$FIRSTITER):1 axis x1y1 with lines title 'Smooth Loss', "
for i in $(seq 1 $CLASS_NUM);
do
    GNUPLOT_CMD="${GNUPLOT_CMD} \"AP"$i".txt\" using (\$0*$MAP_STEP+$FIRSTITER+$MAP_STEP):(\$1*100) axis x1y2 with lines title 'AP "$i"', "
done
GNUPLOT_CMD="${GNUPLOT_CMD} \"mAP.txt\" using (\$0*$MAP_STEP+$FIRSTITER+$MAP_STEP):(\$1*100) axis x1y2 with lines title 'MAP';"

#echo "${GNUPLOT_CMD}"
gnuplot -e "${GNUPLOT_CMD}"

#eog last.png &
