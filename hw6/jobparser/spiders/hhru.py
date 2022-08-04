import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python&items_on_page=20&no_magic=true&L_save_area=true',
        'https://hh.ru/search/vacancy?area=40&search_field=name&search_field=company_name&search_field=description&text=python&items_on_page=20&no_magic=true&L_save_area=true'
    ]

    def parse(self, response: HtmlResponse):
        print('We are here: ', response.url)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        # print(next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, method='GET', callback=self.vacancy_parse)
            # yield response.follow(link, method='GET')


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
