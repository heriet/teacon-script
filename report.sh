#!/bin/bash

if [ $# -ne 2 ]; then
  echo "usage: report.sh <period> <week>"
  exit 1
fi

PERIOD=$1
WEEK=$2

python3 analyze_result.py web/archive/period${PERIOD}/${WEEK}/RESULT > tsv/period${PERIOD}/${WEEK}.tsv
python3 render_report.py ${PERIOD} ${WEEK} tsv/period${PERIOD}/${WEEK}.tsv web/report/period${PERIOD}/${WEEK}.html