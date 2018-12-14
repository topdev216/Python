# -*- coding: utf-8 -*-

from scrapy import Selector
import scrapy
import html2text
import requests
import base64

class IeltsieltsSpider(scrapy.Spider):
    name = 'ielts'
    allowed_domains = ['ieltsielts.com']
    start_urls = ['http://ieltsielts.com/']

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
            text = text.replace(img.extract(), '<img src="data:image/png;base64,%s">' % self._base64_encode(self._download_img(img_url)))
        return Selector(text=text)

    def parse(self, response):
        dom = response.css('div#main div#container div#content')

        for entry in dom.css('div.post'):
            item = {}
            item['entry_header'] = entry.css('div.post h2.entry-title a::text').extract_first()
            item['permalink'] = entry.css('div.post h2.entry-title a::attr(href)').extract_first()
            item['create_at'] = entry.css('div.post div.entry-meta a span::text').extract_first()
            item['category'] = entry.css('div.post div.entry-utility span.cat-links a::text').extract_first()
            html = entry.css('div.entry-content')
            html = self._encode_img(html)
            item['entry_content'] = html2text.html2text(html=html.get(), bodywidth=0)
            yield item

        yield response.follow(response.css('div.navigation div.nav-previous a::attr(href)').extract_first(), self.parse)

