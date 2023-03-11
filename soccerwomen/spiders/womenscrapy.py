import scrapy
import json
from soccerwomen.utils import ListDatesID
from datetime import datetime


class WomenscrapySpider(scrapy.Spider):
    name = 'womenscrapy'
    allowed_domains = ['fifa.com']
    start_urls = ['https://www.fifa.com/api/ranking-overview?locale=en&dateId=ranking_20221209']

    def parse(self, response):
       data = json.loads(response.body)
       items = data['rankings']
       for item in items:
           date_id = response.url.split('_')[-1] # create the date variable from the number id
           date = datetime.strptime(date_id, '%Y%m%d').strftime('%Y-%m-%d')
           country_name = item['rankingItem']['name']
           rank = item['rankingItem']['rank']
           total_points = item['rankingItem']['totalPoints']
           flag = item['rankingItem']['flag']['src']
           conf = item['tag']['id']
           Curl = item['rankingItem']['countryURL']  #complete conutry url
           country_url = 'https://www.fifa.com'+ Curl 
           page_url = response.url  # add page url
           yield {
               'Date': date,
               'Name' : country_name,
               'Rank': rank,
               'Points':total_points,
               'Flag':flag,
               'Conference':conf,
               'CountryUrl' : country_url,
               'PageUrl': page_url 
               }
           
### oon es
           yield from [scrapy.Request(
               url=f'https://www.fifa.com/api/ranking-overview?locale=en&dateId=ranking_{url}', 
               callback = self.parse) for url in ListDatesID]
