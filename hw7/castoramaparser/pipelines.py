# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class CastoramaparserPipeline:
    def process_item(self, item, spider):
        # print('shalomiki')
        return item


class CastoramaparserPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # print('item photos:', item['photos'])
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        # print('item completed')
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item):
        print(request.url)
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        link_name = item["url"].replace("https://www.castorama.ru/", "")
        return f'full/{link_name}/{image_guid}.jpg'
