#!/usr/bin/python
# coding: UTF-8

"""
Teacon Result Report Script

usage:
    python3 analyze_result.py <seq> <input> <output>

example:
    python3 render_report.py 001 tsv/period2/001.tsv web/report/period2/001.html

"""

from jinja2 import Template
import argparse
import csv

import sys
sys.stdin = open(sys.stdin.fileno(),  'r', encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8')
sys.stderr = open(sys.stderr.fileno(), 'w', encoding='utf-8')


def main():

    parser = argparse.ArgumentParser(description='Parser for Teacon')
    parser.add_argument('seq', help='seq (week of teacon)')
    parser.add_argument('input', help='path of tsv')
    parser.add_argument('output', help='path of html')
    args = parser.parse_args()

    seq = args.seq
    input_file = args.input
    output_file = args.output

    tsv = csv.reader(open(input_file, 'r', encoding='utf-8'), delimiter='\t')
    headers = next(tsv)

    players = []
    for row in tsv:
        player = {}

        player['eno'] = row[0]
        player['d04_eno'] = row[0].zfill(4)

        row.pop(0)
        player['data'] = row

        players.append(player)

    template = Template(open('template/report.html', 'r', encoding='utf-8').read())

    template.stream(seq=seq, headers=headers, players=players).dump(output_file)


if __name__ == '__main__':
    main()
