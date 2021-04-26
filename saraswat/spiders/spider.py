import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SaraswatItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class SaraswatSpider(scrapy.Spider):
	name = 'saraswat'
	start_urls = ['https://www.saraswatbank.com/newslist.aspx?id=News']

	def parse(self, response):
		post_links = response.xpath('//a[@class="read_more hover_effect"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//em[@class="newsdate"]/text()').get()
		title = response.xpath('//h4/text()').get()
		content = response.xpath('//div[@class="page_header"]//text()[not (ancestor::em or ancestor::h4)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=SaraswatItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
