#!/usr/bin/env python
#coding:utf-8

import datetime
import re

class Helper(object):
    @staticmethod
    def trans_date(string, spider_name):
        formats = {
            'simon': '%A, %B %d, %Y',
            'ielts': '%d %B %Y',
        }
        return datetime.datetime.strptime(string, formats.get(spider_name, '')).strftime('%Y-%m-%d')

    @staticmethod
    def get_author(spider_name):
        return {
            'simon': 'Simon Corcoran',
            'ielts': 'Ryan',
        }.get(spider_name, '')

    @staticmethod
    def trans_url(string):
        # 去特殊符号
        chars = ['\'', ':', '"', '!', '?', '.', ',', '\\', '/']
        for char in chars:
            string = string.replace(char, '') if char in string else string
        return '-'.join(re.sub(' +', ' ', string).split(' '))

