import feedparser
import webbrowser
import re

feed = feedparser.parse("https://pub.kb.fortinet.com/rss/firmware.xml")
feed_entries = feed.entries

model = ['FGT_60F', 'FGT_100F', 'FGT_2000E']

for entry in feed.entries:
    article_title = entry.title
    article_link = entry.link
    article_published_at = entry.published # Unicode string
    article_published_at_parsed = entry.published_parsed # Time object
    content = entry.summary

    for x in model:
        pattern = bool(re.findall('FortiOS [0-9]+\.+[0-9]+\.[0-9]', article_title))
        if pattern == True:
            #print("{} [{}]".format(article_title, article_link))
            #print("Published at {}".format(article_published_at))
            #print("Content {}".format(content))
            #print(30*'#')
            
            if x in content:
                print(f'New firmware for {x} is available - {article_title}')


        
