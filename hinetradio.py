#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import ujson

from docopt import docopt
from subprocess import Popen

option = """
Usage:
  hinetradio <channel>
  hinetradio (-l | --list)
  hinetradio (-a | --all)
"""

CHANNEL_URL = "http://hichannel.hinet.net/radio/play.do?id={}"
LIST_PATTERN = "http://hichannel.hinet.net/radio/channelList.do?radioType=&freqType=&freq=&area=&pN={}"

headers = {
    'Referer': 'http://hichannel.hinet.net/radio/index.do',
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
}


def getRadioLink(id):
    r = requests.get(CHANNEL_URL.format(id), headers=headers).content.decode('utf-8')
    if r != u'{"msg":"請選擇電台"}':
        data = ujson.loads(r)
        return data['channel_title'], data['playRadio'], data['programName']
    return None


def getPageSize():
    data = requests.get(LIST_PATTERN.format(1)).json()
    return data['pageNo'], data['pageSize']


def getRadioList(start, end):
    radioList = []
    for i in range(start, end+1):
        r = requests.get(LIST_PATTERN.format(i)).content.decode('utf-8')
        data = ujson.loads(r)
        for item in data['list']:
            if item['isChannel'] == True:
                radio = (item['channel_id'], item['channel_title'])
                radioList.append(radio)
    return radioList


def PrintChannel():
    radios = """
     [232] 飛碟電台
     [308] KISS RADIO 網路音樂台
     [156] KISS RADIO 大眾廣播電台
     [340] 佳音現代聖樂網
     [259] 寶島新聲廣播電台
     [357] Flyradio 飛揚調頻
    [1140] 快樂聯播網－台北
    [1120] Classical 台中古典音樂台
    """
    print radios


def PrintList():
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = ['頻道1', '名稱1', '頻道2', '名稱2']
    start, end = getPageSize()
    radioList = getRadioList(start, end)
    length = len(radioList)
    for i in range(0, length, 2):
        x.add_row([radioList[i][0], radioList[i][1], radioList[i+1][0], radioList[i+1][1]])
    print x


if __name__ == "__main__":
    opt = docopt(option, argv=None, help=True)

    if opt['-l'] or opt['--list']:
        PrintChannel()
    elif opt['-a'] or opt['--all']:
        PrintList()
    elif opt['<channel>'] is not None:
        try:
            channel = int(opt['<channel>'])
            info = getRadioLink(channel)
            if not info:
                print u'請輸入電台頻道..'
                PrintChannel()
            else:
                title, url, programName = info
                print u'{1}: 播放{0}'.format(programName, title)
                cmd = "/opt/homebrew-cask/Caskroom/vlc/2.2.1/VLC.app/Contents/MacOS/VLC"
                Popen(['nohup', cmd, url])
        except ValueError:
            print u'請輸入電台頻道..'
            PrintChannel()
    else:
        print opt
