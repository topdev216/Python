#!/usr/bin/env python
#coding: utf-8


import web


urls = (
    '/baidu', 'BaiduTest',
)

class BaiduTest(object):
    def POST(self):
        try:
            with f as open('result.json', 'w'):
                f.write(str(web.input(), encoding='utf8'))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

