import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from collections import namedtuple
from DBCawler.items import DBCrawlerItem
import json
import chardet
import os
import validators
from urllib import request

Node    = namedtuple('Node', ['subs', 'obs'])

class DBCrawler(CrawlSpider):
    name    = 'DBCrawler'
    
    def __init__(self):
        self.root = "http://fragments.dbpedia.org/2016-04/en?"
        self.FB_DBs     = dict()
        self.DBnodes    = dict()
        self.DBnodesP   = dict()
        self.crawled    = dict()
        with open('../../data/FB-DBs(15KOnetoMany)', 'r') as f:
        # with open('../../data/FB-DBs(test)', 'r') as f:
            for l in f:
                items   = l.split()
                fb      = items[0]
                if len(items) > 2:
                    dbs     = items[1:]
                else:
                    dbs     = [items[1]]
                dbs = [i[1:-1] for i in dbs]
                self.FB_DBs.update({fb:dbs})

        # 基本子图 : 完全由记载节点构成的子图
        self.DB15K = open('../../data/DB15K', 'w')
        # 半扩展子图 : 每个triple中只有一个记载节点
        self.DB15KP = open('../../data/DB15K+', 'w')
        # 全扩展子图 : 每个triple中没有记载节点, 但是其中每个点必然可链入基本子图
        self.DB15KPP = open('../../data/DB15K++', 'w')

        # depth=0:可记录半扩展子图 depth>1:可记录全扩展子图 数目为扩展层数
        self.depth = 0
        self.count = 1
        self.count_ = 1
        self.maxPage = 50
        self.jumpNode = False
    def urlConvert(self, dbUrl):
        dbUrl       = dbUrl.replace('/','%2F').replace(':','%3A')
        subjectUrl  = self.root + "subject="+dbUrl+"&predicate=&object="
        objectUrl   = self.root + "subject=&predicate=&object="+dbUrl
        return subjectUrl,objectUrl
    
    def test(self):
        node = "http://dbpedia.org/resource/Americas"
        subjectUrl,objectUrl = self.urlConvert(node)
        yield scrapy.FormRequest(subjectUrl,meta={'layer':2},callback = self.parse)
        yield scrapy.FormRequest(objectUrl, meta={'layer':2} ,callback = self.parse)
		
    def nextPage(self, response):
        signs = response.xpath('//ul[@class="links"]//a/@rel').extract()
        if 'next' in signs:
            link = response.xpath('//ul[@class="links"]//a[@rel="next"]/@href').extract()
            return link[0]
        else:
            return None

    def start_requests(self):
        for fbItem in self.FB_DBs:
            for DBnode in self.FB_DBs[fbItem]:
                self.DBnodes.update({DBnode:1})
        count = 1
        for fbItem in self.FB_DBs:
            for DBnode in self.FB_DBs[fbItem]:
                print(self.count_, '+++',self.count)
                self.count_ += 1
                if DBnode not in self.crawled:
                    self.crawled.update({DBnode:1})
                    subjectUrl,objectUrl = self.urlConvert(DBnode)
                    yield scrapy.FormRequest(subjectUrl,meta={'layer':1},callback = self.parse)
                    yield scrapy.FormRequest(objectUrl, meta={'layer':1} ,callback = self.parse)
                    
    def parse(self, response):
        self.count     += 1
        sel             = scrapy.Selector(response)
        triplesXML      = response.xpath('//ul[@class="triples"]/li').extract()
        triples         = []
        relation_set    = set()
        for tripleXML in triplesXML:
            a = scrapy.Selector(text=tripleXML).xpath('//abbr/@title').extract()
            if len(a)==3:
                triples.append(a)
                relation_set.add(a[1])
            
        relation_set_ = ["wikiPage" in i for i in list(relation_set)]
        if sum(relation_set_) == len(relation_set_):
            print('+++++++++++++++++++')
            print(relation_set)
            print(response.url)
            print('-------------------')
            return
            
            
        for h,r,t in triples:
            if h == t:
                continue
            if (validators.url(t) == False) ^ (validators.url(h) == False):
                continue
            elif (validators.url(t) == False) and (validators.url(h) == False):
                self.jumpNode = True
                return 
            
            if h in self.DBnodes and t in self.DBnodes:
                self.DB15K.write(' '.join([h,r,t])+'\n')
            elif (h in self.DBnodes) ^ (t in self.DBnodes):
                self.DB15KP.write(' '.join([h,r,t])+'\n')
            elif h not in self.DBnodes and t not in self.DBnodes:
                # print(response.url)
                return
                if h in self.DBnodesP and t in self.DBnodesP:
                    self.DB15KP.write(' '.join([h,r,t])+'\n')
                else:
                    self.DB15KPP.write(' '.join([h,r,t])+'\n')
            
            if response.meta['layer'] <= self.depth:
                # print('++++++++++++++++++++')
                if h not in self.DBnodes:
                    self.DBnodesP.update({h:1})
                if t not in self.DBnodes:
                    self.DBnodesP.update({t:1})
                
                if h not in self.crawled and h not in self.DBnodes:
                    self.crawled.update({h:1})
                    subjectUrl,objectUrl = self.urlConvert(h)
                    yield scrapy.FormRequest(subjectUrl, meta={'layer':response.meta['layer']+1} ,callback = self.parse)
                    yield scrapy.FormRequest(objectUrl, meta={'layer':response.meta['layer']+1} ,callback = self.parse)
                if t not in self.crawled and t not in self.DBnodes:
                    self.crawled.update({t:1})
                    subjectUrl,objectUrl = self.urlConvert(t)
                    yield scrapy.FormRequest(subjectUrl, meta={'layer':response.meta['layer']+1} ,callback = self.parse)
                    yield scrapy.FormRequest(objectUrl, meta={'layer':response.meta['layer']+1} ,callback = self.parse)
            
        nextPage = self.nextPage(response)
        if nextPage != None:
            #if int(nextPage.split('=')[-1]) > self.maxPage:
            #    return
            yield scrapy.FormRequest(nextPage, meta={'layer':response.meta['layer']} ,callback = self.parse)