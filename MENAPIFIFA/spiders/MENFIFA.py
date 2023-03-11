import scrapy
import json
from datetime import datetime
from MENAPIFIFA.utils import date_ids


class MenfifaSpider(scrapy.Spider):
    name = 'MENFIFA'
    allowed_domains = ['fifa.com']

     
    def start_requests(self):
        for item in date_ids:
            url = f"https://www.fifa.com/api/ranking-overview?locale=en&dateId={item['id']}"
            date_text = item['text'].replace('Sept', 'sep')
            date_obj = datetime.strptime(date_text, '%d %b %Y')
            date = date_obj.strftime('%Y-%m-%d')
            yield scrapy.Request(url=url, callback=self.parse, meta={'url': url, 'date': date})
                      

    def parse(self, response):
        data = json.loads(response.body)
        url = response.meta['url']
        date = response.meta['date']
        for ranking in data['rankings']:
            ranking['url'] = url
            ranking['date'] = date 
            yield ranking

# 

