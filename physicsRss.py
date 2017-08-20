import feedparser
import pprint

prl_url = "http://feeds.aps.org/rss/allsuggestions.xml"
sci_url = "http://advances.sciencemag.org/rss/current.xml"
feeds = feedparser.parse(sci_url)

data = []
count = 0
with open("{0}.data".format("sci_url"), 'w') as f:
    for entry in feeds.entries:
        
        title = entry.title.encode('utf-8')
        description = entry.description
        start = description.find('<p>')+3
        end = description.find('</p>')
        para = description[start:end].encode('utf-8')
        link = entry.link
        print entry.authors
        
        record = "title" + str(count)+':\n' + title + '\n'+ \
                "description"+str(count)+':\n' + para + '\n' +\
                 "link"+str(count)+link+':\n'
                        
        f.writelines(str(record)+'\n')
    
        count += 1
