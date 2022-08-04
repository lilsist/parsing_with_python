import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response):
        print('We are here: ', response.url)
        next_page = response.xpath('//a[@class="_1IHWd _6Nb0L _37aW8 _3187U f-test-button-dalshe f-test-link-Dalshe"]/@href').get()
        #print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//span[@class='_2TI7V _21QHd _36Ys4 _3SmWj']/a/@href").getall()
        for link in links:
            yield response.follow(link, method='GET', callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath('//span[@class="_2eYAG _10_Fa _21QHd _9Is4f"]//text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
