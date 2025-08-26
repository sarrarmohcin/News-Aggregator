import feedparser
import json
import validators
from datetime import datetime
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

# get feature from item
def get_feature(feature,data):

    if feature in data:
        return data[feature]
    else:
        return ''
    
    
# get url from item
def get_url(result):

    if validators.url(get_feature('link',result)):
        return get_feature('link',result)
    elif validators.url(get_feature('id',result)):
        return get_feature('id',result)
    elif 'links' in result and validators.url(get_feature('href',result['links'][0])):
        return get_feature('href',result['links'][0])
    else:
        return ""

 # get date from item
def get_date(published):
    
    if published == '':
        published_timestamp = datetime.now()
    else:
        published_timestamp = datetime(published[0], published[1], published[2],published[3] , published[4] , published[5]) 
    
    return int(datetime.timestamp(published_timestamp))


# get list of values from item
def get_list(parent_feature,child_feature,data):
    if parent_feature in data:
        tags = []
        for element in data[parent_feature]:
            if child_feature in element:
                tags.append(element[child_feature])
        return tags
    else:
        return []
    
    
    
# get medi from item
def get_media_content(result,summary,content):

    if 'media_content' in result and get_feature('url',result['media_content'][0]) != "":
        return get_feature('url',result['media_content'][0])
    elif 'media_thumbnail' in result and get_feature('url',result['media_thumbnail'][0])!= "":
        return get_feature('url',result['media_thumbnail'][0])
    elif 'links' in result and len(result['links'])>1:
        if get_feature('href',result['links'][1])!= "":
            return get_feature('href',result['links'][1])
    elif extract_images(summary):
        return extract_images(summary)[0]
    elif extract_images(content):
        return extract_images(content)[0]
    else:
        return ""
    
# extract image from html content inside article content
def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    imgs = []
    if images:
        for img in images:
            if img.has_attr('src'):
                imgs.append(img['src'])
    return imgs
    
# remove html tags from content
def remove_tags(raw_text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', raw_text)
# main
def read():
    # Open and read a JSON file
    with open("newspapers.json", "r") as f:
        newspapers = json.load(f)
    
    data = []
    for paper in newspapers:
        # read RSS using feedparse
        rss = feedparser.parse(paper['url'])
        results = rss['entries']
        
        # test if result is not None or empty
        if results is None or not isinstance(results, list) or len(results) == 0 :
            print(f"Empty results from RSS feed")
            continue
        
        for result in results:
            # get the article url
            url = get_url(result)
            
            # test if article has a valid url
            if url is None or url == "":
                print('article without url')
                continue
            
            # get others features
            pubdate = get_date(get_feature('published_parsed',result))
            title = get_feature('title',result)
            author = get_feature('author',result)
            tags = get_list('tags','term',result)
            summary = get_feature('summary',result)
            content = get_feature('value',result['content'][0]) if get_feature('content',result) else ''
            media_content = get_media_content(result,summary,content)
            
            # clean article content
            content_final  = ""
            if(content != ''):
                content_final = remove_tags(content)
            elif(summary != ''):
                content_final = remove_tags(summary)
            else:
                content_final = ''
                
            
            # create article Dict
            article = {
                'newspaper' : paper['name'],
                'title' : title,
                'published' : pubdate,
                'url' : url, 
                'tags' : tags,
                'author' : author,
                'content' :  content_final,
                'media' : media_content,
            }
            
            data.append(article)
    
    store(data)
    return data


def store(data):
    # Load existing CSV
    csv_file = "articles.csv"
    
    # Check if file exists
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        # Create empty DataFrame with the columns you expect
        df = pd.DataFrame(columns=["newspaper", "title", "published","url","tags","author","content","media"])
    
    # Convert new data into DataFrame
    new_df = pd.DataFrame(data)
    
    # Merge: update existing rows and append new ones
    # 'url' is the unique key
    df = pd.concat([df, new_df]).drop_duplicates(subset=["url"], keep="last")

    # Save back to CSV
    df.to_csv(csv_file, index=False)

data = read()

print(data)