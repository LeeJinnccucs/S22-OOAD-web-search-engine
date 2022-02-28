import scrapy
import time

class moviespider(scrapy.Spider):
	name = 'movie'
	start_urls = ['https://en.wikipedia.org/wiki/List_of_American_films_of_2021']

	def parse(self, response):
		for link in response.css('table.wikitable.sortable a::attr(href)'):
			yield response.follow('https://en.wikipedia.org/'+link.get(), callback=self.parse_plot)
	
	def parse_plot(self, response):
		movie = response.css('div#content')
		yield {
			'name': movie.css('i::text').get(),
			'plot': ' '.join(t.strip() for t in response.css('div.mw-parser-output p::text, div.mw-parser-output p ::text').extract()).strip(),
		}
