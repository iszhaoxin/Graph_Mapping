import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DbcawlerPipeline(object):
    def open_spider(self, spider):
        self.DBnodesfn  = open('../../data/DBnodesfn.json', 'w')
        self.DBnodesPfn = open('../../data/DBnodesPfn.json', 'w')
        self.crawledfn  = open('../../data/crawled.json', 'w')

    def close_spider(self, spider):
        for i in spider.DBnodes:
            self.DBnodesfn.write(str(i)+'\n')
        for i in spider.DBnodesP:
            self.DBnodesPfn.write(str(i)+'\n')
        for i in spider.crawled:
            self.crawledfn.write(str(i)+'\n')
        
        self.DBnodesfn.close()
        self.DBnodesPfn.close()
        self.crawledfn.close()

    def process_item(self, item, spider):
        return item
