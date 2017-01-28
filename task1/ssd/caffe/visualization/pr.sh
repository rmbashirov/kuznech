#!/bin/bash

# requires: gnuplot, gnuplot-x11
# usage: ./pr.sh CLASS_NUM OUT_DIR

set -e
# set -o xtrace

if [ "$#" -ne 2 ]
then
    echo "usage: ./pr.sh CLASS_NUM OUT_DIR"
    exit
fi

REL_PATH_TO_SCRIPT=$(dirname "${BASH_SOURCE[0]}")
cd "${REL_PATH_TO_SCRIPT}"	# it's possible to run the script from some other dir, it can to "cd" on its own

CLASS_NUM="$1"
OUT_DIR="$2"
mkdir -p "./${OUT_DIR}"

for CLASS_IDX in $(seq 1 $CLASS_NUM);
do
	IN_FILE="../torun/last_prec_rec/label_${CLASS_IDX}.txt"
	if [ ! -f "${IN_FILE}" ]
	then
	    echo "File not found: ${IN_FILE}"
	    exit
	fi

	GNUPLOT_CMD="set term png size 1024,1024 enhanced; set output \"./${OUT_DIR}/pr_${CLASS_IDX}.png\"; set xrange [0:1]; set yrange [0:1]; set grid xtics lt 0; set grid ytics lt 0; set grid y2tics lt 0; set tics out; set xlabel 'Recall'; set ylabel 'Precision'; plot"
	GNUPLOT_CMD="${GNUPLOT_CMD} \"${IN_FILE}\" using 3:2 axis x1y1 with lines title 'Precision', "
	GNUPLOT_CMD="${GNUPLOT_CMD} \"${IN_FILE}\" using 3:1 axis x1y1 with lines title 'Confidence';"

	#echo "${GNUPLOT_CMD}"
	gnuplot -e "${GNUPLOT_CMD}"
done
