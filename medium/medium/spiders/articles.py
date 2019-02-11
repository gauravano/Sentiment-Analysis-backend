# -*- coding: utf-8 -*-
import scrapy, pdb

class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['medium.com']
    
    def __init__(self, *args, **kwargs): 
      super(ArticlesSpider, self).__init__(*args, **kwargs) 
      self.start_urls = [kwargs.get('search_url')]

    def parse(self, response):
        basOrNahi = False
        urls = response.css(
            'div.postArticle-content>a[data-action="open-post"]::attr(href)').extract()
        print(len(urls))
        ids = response.css(
            'div.postArticle-content>a[data-action="open-post"]::attr(data-post-id)').extract()
        for url in urls:
            yield(scrapy.Request(url=url, callback=self.parse_article))
        # if(not basOrNahi):
        #     query = 'https://medium.com/search/posts?q=biometric%20security&count=10'
        #     for id in ids:
        #         query = query + '&ignore=' + id
        #     basOrNahi = True
        #     yield(scrapy.Request(url=query, callback=self.parse))

    def parse_article(self, response):
        content = response.css('.sectionLayout--insetColumn ::text').extract()
        article = ''.join(content)
        yield({
            'title': content[0],
            'text': article
        })
