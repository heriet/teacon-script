#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Teacon Result Analyze Script

usage:
    python3 analyze_result.py <dir>

    <dir>: Teacon RESULT dir (ex. "./001/RESULT" )


example:
    python3 analyze_result.py web/archive/period2/001/RESULT > tsv/period2/001.tsv

"""


import codecs
import re
import glob
import os
import argparse
from bs4 import BeautifulSoup

import sys
sys.stdin = open(sys.stdin.fileno(),  'r', encoding='utf-8')
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-8')
sys.stderr = open(sys.stderr.fileno(), 'w', encoding='utf-8')


class Player:
    def __init__(self):
        self.eno = ''
        self.name = ''
        self.nickname = ''
        self.acc_tp = 0
        self.acc_cp = 0
        self.acc_kp = 0
        self.tp = 0
        self.cp = 0

        self.hostility = 0
        self.vanity = 0
        self.suspicious = 0
        self.selfish = 0
        self.pride = 0
        self.magic = 0

        self.money = 0
        self.exp = 0
        self.dangerous = 0


class Fortress:
    def __init__(self):
        self.eno = ''

        self.magnificent = 0
        self.story = 0
        self.caution = 0

        self.at_delay = 0
        self.at_accel = 0
        self.at_lead = 0

        self.df_delay = 0
        self.df_accel = 0
        self.df_lead = 0
        self.df_fight = 0
        self.df_shoot = 0
        self.df_magic = 0

        self.used_magic = 0
        self.status = ''


class Result:
    def __init__(self):
        self.eno = ''
        self.interest_tp = 0
        self.interest_cp = 0
        self.get_tp = 0
        self.get_cp = 0
        self.get_kp = 0
        self.sell = 0
        self.sell_exp = 0
        self.issue = ''

        self.player = None
        self.fortress = None


def get_tag_content(soup):

    if not soup:
        return ''

    text = ''.join([
        s.string.strip() if s.string else str(s) for s in soup.contents])
    return text


def read_result(input_dir, eno):

    try:
        file = codecs.open(os.path.join(input_dir, 'c%04d.html' % eno), 'r')
    except IOError:
        return None

    html = file.read()
    file.close()

    return html


def analyze_result(input_dir, eno):

    html = read_result(input_dir, eno)

    if not html:
        return None

    try:
        soup = BeautifulSoup(html, 'lxml')
    except Exception:
        return None

    result = Result()
    result.eno = eno

    harvest_div = soup.find('h2', {'id': 'nextday'}).find_next_sibling('div')
    harvest_p = harvest_div.find('p')

    for index in range(len(harvest_div.contents)):
        element = harvest_div.contents[index]

        if not element.string:
            continue

        if re.search(r'TP蓄積増加', element.string):
            result.interest_tp = int(harvest_div.contents[index+1].contents[0]) if len(harvest_div.contents[index+1].contents) > 0 else 0

        if re.search(r'CP蓄積増加', element.string):
            result.interest_cp = int(harvest_div.contents[index+1].contents[0]) if len(harvest_div.contents[index+1].contents) > 0 else 0

    for index in range(len(harvest_p.contents)):
        element = harvest_p.contents[index]

        if not element.string:
            continue

        if re.search(r'TP収穫', element.string):
            result.get_tp = int(harvest_p.contents[index+1].contents[0]) if len(harvest_p.contents[index+1].contents) > 0 else 0

        if re.search(r'CP収穫', element.string):
            result.get_cp = int(harvest_p.contents[index+1].contents[0]) if len(harvest_p.contents[index+1].contents) > 0 else 0

        if re.search(r'KP変異', element.string):
            result.get_kp = int(harvest_p.contents[index+1].contents[0]) if len(harvest_p.contents[index+1].contents) > 0 else 0

        if re.search(r'販売経験', element.string):
            text = harvest_p.contents[index+1].contents[0]
            match = re.match(r'(\d+)\s*\(売上(\d+)個\)', text)
            result.sell_exp = int(match.group(1))
            result.sell = int(match.group(2))

    # Player
    charadata = soup.find('table', {'class': 'charadata'})
    player = Player()
    player.eno = eno
    player.name = charadata.find('th', text='名前').next_sibling.string
    player.nickname = charadata.find('th', text='愛称').next_sibling.string

    player.acc_tp = int(charadata.find('th', text='累積TP').next_sibling.string)
    player.acc_cp = int(charadata.find('th', text='累積CP').next_sibling.string)
    player.acc_kp = int(charadata.find('th', text='累積KP').next_sibling.string)

    player.tp = int(charadata.find('th', text='TP').next_sibling.string)
    player.cp = int(charadata.find('th', text='CP').next_sibling.string)

    player.hostility = int(charadata.find('th', text='敵愾心').next_sibling.string)
    player.vanity = int(charadata.find('th', text='虚栄心').next_sibling.string)
    player.suspicious = int(charadata.find('th', text='猜疑心').next_sibling.string)
    player.selfish = int(charadata.find('th', text='利己心').next_sibling.string)
    player.pride = int(charadata.find('th', text='自尊心').next_sibling.string)
    player.magic = int(charadata.find('th', text='魔力').next_sibling.string)

    player.money = int(charadata.find('th', text='money').next_sibling.string)
    player.exp = int(charadata.find('th', text='経験値').next_sibling.string)
    player.dangerous = int(charadata.find('th', text='危険度深度').next_sibling.string)

    # Fortress
    specdata = soup.find('table', {'class': 'specdata'})
    fortress = Fortress()
    fortress.eno = eno

    if specdata:
        fortress.magnificent = int(specdata.find('th', text='壮大値').next_sibling.string)
        fortress.story = int(specdata.find('th', text='階層数').next_sibling.string)
        fortress.caution = int(specdata.find('th', text='警戒値').next_sibling.string)

        fortress.at_delay = int(specdata.find('th', text='遅延強化').next_sibling.string)
        fortress.at_accel = int(specdata.find('th', text='加速強化').next_sibling.string)
        fortress.at_lead = int(specdata.find('th', text='誘発強化').next_sibling.string)

        fortress.df_delay = int(specdata.find('th', text='遅延防御').next_sibling.string)
        fortress.df_accel = int(specdata.find('th', text='加速防御').next_sibling.string)
        fortress.df_lead = int(specdata.find('th', text='誘発防御').next_sibling.string)
        fortress.df_fight = int(specdata.find('th', text='格闘防御').next_sibling.string)
        fortress.df_shoot = int(specdata.find('th', text='射撃防御').next_sibling.string)
        fortress.df_magic = int(specdata.find('th', text='魔術防御').next_sibling.string)

        fortress.used_magic = int(re.match(r'(\d+)/\d+', specdata.find('th', text='魔力消費量').next_sibling.string).group(1))
        fortress.status = specdata.find('th', text='城塞状況').next_sibling.string

    lose_message = soup.find('i', text='%sの城は陥落した！！' % player.name)
    if lose_message:
        result.issue = '陥落'

    result.player = player
    result.fortress = fortress

    return result


def print_header():

    header = [
        'ENo', '名前', '愛称',
        'TP蓄積増加', 'CP蓄積増加', 'TP収穫', 'CP収穫', 'KP変異',
        'TP+CP収穫', '販売経験', '売上', '戦績',
        '累積TP', '累積CP', '累積KP', 'TP', 'CP',
        '敵愾心', '虚栄心', '猜疑心', '利己心', '自尊心',
        'money', '経験値', '危険度深度',
        '壮大値', '階層数', '警戒値',
        '遅延強化', '加速強化', '誘発強化',
        '遅延防御', '加速防御', '誘発防御',
        '格闘防御', '射撃防御', '魔術防御',
        '魔力消費量', '魔力', '城塞状況'
    ]

    print('\t'.join([str(col) for col in header]))


def print_result(result):

    player = result.player
    fortress = result.fortress

    row = [
        player.eno, player.name, player.nickname,
        result.interest_tp, result.interest_cp, result.get_tp, result.get_cp, result.get_kp,
        result.get_tp + result.get_cp, result.sell_exp, result.sell, result.issue,
        player.acc_tp, player.acc_cp, player.acc_kp, player.tp, player.cp,
        player.hostility, player.vanity, player.suspicious, player.selfish, player.pride,
        player.money, player.exp, player.dangerous,
        fortress.magnificent, fortress.story, fortress.caution,
        fortress.at_delay, fortress.at_accel, fortress.at_lead,
        fortress.df_delay, fortress.df_accel, fortress.df_lead,
        fortress.df_fight, fortress.df_shoot, fortress.df_magic,
        fortress.used_magic, player.magic, fortress.status
    ]

    print('\t'.join([str(col) for col in row]))


def trim_result_filename(filename):
    match = re.search(r'c(\d+)\.html', filename)
    return int(match.group(1)) if match else 0


def get_last_eno(input_dir):
    file_list = glob.glob(os.path.join(input_dir, 'c*.html'))

    if len(file_list) == 0:
        sys.exit('Missing result file: c*.html')

    file_no_list = [trim_result_filename(x) for x in file_list]

    file_no_list.sort(reverse=True)
    return file_no_list[0]


def main():

    parser = argparse.ArgumentParser(description='Parser for Teacon')
    parser.add_argument('dir', help='path of RESULT dir')
    args = parser.parse_args()

    input_dir = args.dir
    first_eno = 1
    last_eno = get_last_eno(input_dir)

    print_header()

    for eno in range(first_eno, last_eno + 1):
        result = analyze_result(input_dir, eno)
        print_result(result)

if __name__ == '__main__':
    main()
