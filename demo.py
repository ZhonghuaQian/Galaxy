# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 20:32:50 2017

@author: qzhoo
"""
# -*- coding:utf-8 -*-
import feedparser
from pymongo import MongoClient
import csv
import pprint
import datetime

filename = "rss_sources.csv"

def rssDict(filename):
    '''
    根据filename中rss源，生成列表[{"rss sources":"journal", "url": "http://"}...]
    '''
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            data.append(r)
        return data

def get_doc(journal, url):
    '''
    '''
    feeds = feedparser.parse(url)
    try:
        doc = []
        for entry in feeds.entries:
            
            title = entry.title.encode('utf-8') #get title
            description = entry.description
            start = description.find('<p>')+3
            end = description.find('</p>')
            abstract = description[start:end].encode('utf-8') #get abstract
            link = entry.link.encode('utf-8') # get link
            authors = entry.authors[0]['name'] #get authors
            
            item = {"journal": journal,
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "link": link}
            doc.append(item)
        return doc
    
    except ValueError :
        print "Url is not valid!"
        return None
            
    
    
    
def write2db(journal, url):
    '''
    
    '''
    
    client = MongoClient('mongodb://localhost:27017')
    db = client.physicsRss
    today = str(datetime.date.today()).replace('-', '_')
    collection = db[today]
    document = get_doc(journal, url)
    collection.ensure_index({"title":1},{"unique": True})
    collection.insert_many(document)
    print collection.find().count()
    
def print_db():
    client = MongoClient('mongodb://localhost:27017')
    db = client.physicsRss
    today = str(datetime.date.today()).replace('-', '_')
    collection = db[today]
    with open("test.txt", 'w') as f:
        for doc in collection.find():
            f.writelines(str(doc).encode('utf-8'))
        
    
    
if __name__ == "__main__":
    data = rssDict(filename)
    if data == None:
        print "Rss sources file error!"
    
    for item in  data:
        write2db(item["journal"], item["url"])
    #print_db()