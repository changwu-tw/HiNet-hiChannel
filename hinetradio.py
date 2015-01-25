#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ujson
import urllib2

from docopt import docopt
from subprocess import call


option = """
Usage:
  hinetradio <channel>
  hinetradio (-l | --list)
  hinetradio (-a | --all)
"""

CHANNEL_URL = "http://hichannel.hinet.net/radio/play.do?id={}"
LIST_PATTERN = "http://hichannel.hinet.net/radio/channelList.do?radioType=&freqType=&freq=&area=&pN={}"


def getRadioLink(id):
    json = urllib2.urlopen(CHANNEL_URL.format(id)).read()
    if json != '{"msg":"請選擇電台"}':
        data = ujson.loads(json)
        return data['channel_title'], data['playRadio']
    return None


def getPageSize():
    json = urllib2.urlopen(LIST_PATTERN.format(1)).read()
    data = ujson.loads(json)
    return data['pageNo'], data['pageSize']


def getRadioList(start, end):
    radioList = []
    for i in range(start, end+1):
        json = urllib2.urlopen(LIST_PATTERN.format(i)).read()
        data = ujson.loads(json)
        for item in data['list']:
            if item['isChannel'] == True:
                radio = "[%s] %s" % (item['channel_id'], item['channel_title'])
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
    start, end = getPageSize()
    list = getRadioList(start, end)
    for l in list:
        print l


if __name__ == "__main__":
    opt = docopt(option, argv=None, help=True)

    if opt['-l'] or opt['--list']:
        PrintChannel()
    elif opt['-a'] or opt['--all']:
        PrintList()
    elif opt['<channel>'] is not None:
        try:
            channel = int(opt['<channel>'])
            if not getRadioLink(channel):
                print('請輸入電台頻道..')
                PrintChannel()
            else:
                title, url = getRadioLink(channel)
                print "Playing %s" % title
                cmd = "/opt/homebrew-cask/Caskroom/vlc/2.1.5/VLC.app/Contents/MacOS/VLC"
                call([cmd, url])
        except ValueError:
            print('請輸入電台頻道..')
            PrintChannel()
    else:
        print opt
