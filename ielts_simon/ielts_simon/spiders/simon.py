# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
import html2text
import requests
import base64
import re

class IeltsSpider(scrapy.Spider):
    name = 'simon'
    allowed_domains = ['ielts-simon.com']
    start_urls = ['http://ielts-simon.com/']

    def _download_img(self, url):
        return requests.get(url=url, timeout=60).content

    def _base64_encode(self, bytes):
        return base64.b64encode(bytes).decode('utf8')

    def _encode_img(self, node):
        imgs = node.css('img')
        if not imgs: return node
        text = node.get()
        for img in imgs:
            img_url = img.css('img::attr(src)').extract_first()
            text = text.replace(img.extract(), '<img src="data:image/jpg;base64,%s">' % self._base64_encode(self._download_img(img_url)))
        return Selector(text=text)

    def _filt_noise(self, node):
        text = ''
        for line in node.get().splitlines():
            if '#ffffff' in line.lower():
                line = re.sub(r'\<span\ style\=\"color\:\ \#ffffff\;\"\>\w+\<\/span\>', '', line)
            line = line.strip()
            if len(line) > 0: text += line + '\n'
        return Selector(text=text)

    def parse(self, response):
        for i in range(len(response.css('h2.date-header'))):
            item = {}

            item['create_at'] = response.css('h2.date-header::text').extract()[i]

            entry = response.css('div.entry')[i].css('div.entry-inner')
            item['entry_header'] = entry.css('div.entry-inner h3.entry-header a::text').extract_first()

            html = entry.css('div.entry-inner div.entry-content div.entry-body')
            html = self._encode_img(html)
            html = self._filt_noise(html)
            item['entry_content'] = html2text.html2text(html=html.get(), bodywidth=0)

            item['category'] = ', '.join(entry.css('div.entry-inner div.entry-footer p.entry-footer-info span.post-footers a::text').extract())[7:]
            item['permalink'] = entry.css('p.entry-footer-info a.permalink::attr(href)').extract_first()

            self.logger.info('>>> ' + item['permalink'])
            yield item

        self.logger.info('starting to crawl next page...')
        yield response.follow(response.css('div.pager div.pager-inner span.pager-right a::attr(href)').extract_first(), self.parse)
