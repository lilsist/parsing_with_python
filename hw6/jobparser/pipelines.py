# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies0508

    def process_item(self, item, spider):
        salary_from_spider = item['salary']
        if spider.name == 'hhru':
            item['salary'] = self.process_salary_hh(salary_from_spider)
        elif spider.name == 'superjob':
            item['salary'] = self.process_salary_sj(salary_from_spider)
        else:
            print('Not existing spider')
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        #return item

    def process_salary_hh(self, salary: list):
        if salary[0] == 'з/п не указана':
            min_salary = None
            max_salary = None
            currency = None
        elif salary[0] == 'от ' and salary[2] == ' до ':
            min_salary = int(salary[1].replace('\xa0', ''))
            max_salary = int(salary[3].replace('\xa0', ''))
            currency = salary[5]
        elif salary[0] == 'от ' and salary[2] == ' ':
            min_salary = int(salary[1].replace('\xa0', ''))
            max_salary = None
            currency = salary[3]
        elif salary[0] == 'до ':
            min_salary = None
            max_salary = int(salary[1].replace('\xa0', ''))
            currency = salary[3]
        else:
            print('another case')
            min_salary = None
            max_salary = None
            currency = None
        return min_salary, max_salary, currency

    def process_salary_sj(self, salary: list):
        #print(salary)
        if salary[0] == 'По договорённости':
            min_salary = None
            max_salary = None
            currency = None
        elif salary[2] == '—': # от до
            min_salary = int(salary[0].replace('\xa0', ''))
            max_salary = int(salary[4].replace('\xa0', ''))
            currency = salary[6]
        elif salary[0] == 'от': # от
            min_salary = int(salary[2].replace('\xa0', '').replace('руб.', ''))
            max_salary = None
            currency = 'руб.'
        elif salary[1] == '\xa0': # до
            min_salary = None
            max_salary = int(salary[0].replace('\xa0', ''))
            currency = salary[2]
        elif salary[0] == 'до': # до2
            min_salary = None
            max_salary = int(salary[2].replace('\xa0', ''))
            currency = 'руб.'
        else:
            print('another case')
            min_salary = None
            max_salary = None
            currency = None

        return min_salary, max_salary, currency
