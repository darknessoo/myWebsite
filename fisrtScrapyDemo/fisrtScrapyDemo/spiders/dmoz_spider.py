#! encoding=utf-8
# @Time    : 2018/5/5 16:02
# @Author  : lhy

import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.runoob.com/regexp/",
        "https://morvanzhou.github.io/"
    ]

    # def parse(self, response):
    #     filename = response.url.split("/")[-2]
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
        yield {  # return some results
            'title': response.css('h1::text').extract_first(default='Missing').strip().replace('"', ""),
            'url': response.url,
        }

        urls = response.css('a::attr(href)').re(r'^/.+?/$')  # find all sub urls
        for url in urls:
            yield response.follow(url, callback=self.parse)  # it will filter duplication automatically