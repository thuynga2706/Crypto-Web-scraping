#!/usr/bin/env python
# coding: utf-8

# ## Automated Content Generating AI (Using Vader NLP) for Marketing Team 

# In[1]:


import re
import pandas as pd
import numpy as np
import requests
import warnings
from bs4 import BeautifulSoup as bs
import warnings
import datetime as dt
from datetime import timedelta

warnings.filterwarnings("ignore")

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}


# ## Done: Live Coin Watch, Coindesk, Forexlive, BBC, Cointelegraph,Techbullion, Venturebeat, Dailyfintech, Breakermag, Quartz, Coinspeaker, Cryptocompare
# 

# In[2]:


olddata=pd.read_json('dataset.json')
oldlinks = olddata['Links']


# # Live Coin Watch
# 

# In[3]:


articles = [[],[],[],[],[],[]]

url = "https://news.livecoinwatch.com/"

response = requests.get(url, headers)
soup = bs(response.text, "lxml")

x = soup.find_all('h3')
for rawlink in x:
    link = rawlink.find('a').get('href')
    if link not in set(oldlinks):
        try:
            articlesoup = bs(requests.get(link).text, 'html.parser')
            #if timestamp>time:
            articletext = articlesoup.article.find('div','td-post-content').get_text(' ', strip=True)
            wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
            words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
            articles[0].append(articlesoup.find('title').get_text())
            articles[1].append(pd.Timestamp(articlesoup.article.find('time').get_text()))
            articles[2].append(link)
            articles[3].append(articletext)
            articles[4].append(wordslength)
            articles[5].append(words) ### Use to collect all words splitted already for NLP
        except:
            pass


livecoinwatch = pd.DataFrame()

livecoinwatch['Title'], livecoinwatch['Timestamp'], livecoinwatch['Links'], livecoinwatch['Text'], livecoinwatch['Wordslength']  = articles[0],pd.to_datetime(articles[1]),articles[2],articles[3],articles[4]


# # Scrape Forexlive

# In[4]:


articles = [[],[],[],[],[],[]]
url = "https://www.forexlive.com/Cryptocurrency"
response = requests.get(url, headers)
soup = bs(response.text, 'lxml')
x = soup.find_all('article')
for rawlink in x:
        link = 'https:' + rawlink.find('a').get('href')
        if link not in set(oldlinks):
            try:
                articlesoup = bs(requests.get(link, headers=headers).text, 'html.parser')
                articletext = articlesoup.article.find_all('div','artbody')[0].get_text(' ', strip=True)
                words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
                wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
                articles[0].append(articlesoup.find('title').get_text())
                articles[1].append(pd.to_datetime(articlesoup.article.find_all('time')[1].get_text()))
                articles[2].append(link) 
                articles[3].append(articletext)
                articles[4].append(wordslength)
                articles[5].append(words) ### Use to collect all words splitted already for NLP
            except:
                pass
    
    
forexlive = pd.DataFrame()
forexlive['Title'], forexlive['Timestamp'], forexlive['Links'], forexlive['Text'], forexlive['Wordslength']  = articles[0],pd.to_datetime(articles[1]),articles[2],articles[3],articles[4]


# # Scrape Coindesk

# In[5]:


articles = [[],[],[],[],[],[]]
url = "https://www.coindesk.com/"
response = requests.get(url, headers)
soup = bs(response.text, 'lxml')
x=soup.find('div',id='body-container').find_all('a')
for rawlink in x:
    link = rawlink.get('href')
    if link not in set(oldlinks):
        try:
            articlesoup = bs(requests.get(link).text, 'html.parser')
            articletext = articlesoup.find_all('div','entry-content')[0].get_text(' ', strip=True)
            wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
            words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
            articles[0].append(articlesoup.find('title').get_text())
            articles[1].append(pd.to_datetime(articlesoup.article.find("div",'timestamp').find("span").get_text()))
            articles[2].append(link)
            articles[3].append(articletext)
            articles[4].append(wordslength)
            articles[5].append(words) ### Use to collect all words splitted already for NLP
        except:
            pass
            

coindesk = pd.DataFrame()
coindesk['Title'], coindesk['Timestamp'], coindesk['Links'], coindesk['Text'], coindesk['Wordslength']  = articles[0],pd.to_datetime(articles[1]),articles[2],articles[3],articles[4]


# # Cointelegraph

# In[6]:


import feedparser

articles = [[],[],[],[],[],[]]
url = "https://cointelegraph.com/rss"
response = feedparser.parse(url)

for rawlink in response.entries:
    link = rawlink['link']
    if link not in set(oldlinks):
        try:
            
            articles[0].append(rawlink["title"])
            articles[1].append(pd.to_datetime(rawlink['published']))
            articles[2].append(link)
            articlesoup = bs(requests.get(link, headers=headers).text, 'html.parser')

            p = articlesoup.find_all('div','post-full-text contents js-post-full-text')
            if len(p) > 0:
                articletext = p[0].get_text(' ', strip=True)
                wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
                words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
                articles[3].append(articletext)
                articles[4].append(wordslength)
                articles[5].append(words) ### Use to collect all words splitted already for NLP
            else:
                p=articlesoup.find('div','content_block__inner col-xs-12 col-sm-12 col-md-8 col-lg-8 pull-right')
                articletext = p.get_text(' ', strip=True)
                wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
                words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
                articles[3].append(articletext)
                articles[4].append(wordslength)
                articles[5].append(words) 

        except:
            pass

        
cointelegraph = pd.DataFrame()
cointelegraph['Title'], cointelegraph['Timestamp'], cointelegraph['Links'], cointelegraph['Text'], cointelegraph['Wordslength']  = articles[0],pd.to_datetime(articles[1]),articles[2],articles[3],articles[4]


# # Not pulled from: Coinstats, CoinGecko, Messari, NewsAPI, Coinlore

# # Crypto compare

# In[7]:


from urllib.request import *
from datetime import datetime
import json

coinlisthttps = urlopen("https://min-api.cryptocompare.com/data/v2/news/?lang=EN").read().decode('utf-8')
coinlistdata = json.loads(coinlisthttps)["Data"]

articles = [[],[],[],[],[],[]]
for rawlink in coinlistdata:    
    link = rawlink["url"]
    if link not in set(oldlinks):
        articles[0].append(rawlink["title"])
        articles[1].append(datetime.fromtimestamp(rawlink["published_on"]).strftime('%Y-%m-%d %H:%M:%S'))
        articles[2].append(link)
        articles[3].append(rawlink["body"])
        wordslength = len(re.sub('[^a-z\ \']+', ' ',  rawlink["body"]).split())
        words = re.sub('[^a-z\ \']+', ' ',  rawlink["body"]).split()
        articles[4].append(wordslength)
        articles[5].append(words) ### Use to collect all words splitted already for NLP

        
cryptocompare = pd.DataFrame()
cryptocompare['Title'], cryptocompare['Timestamp'], cryptocompare['Links'], cryptocompare['Text'], cryptocompare['Wordslength']  = articles[0],articles[1],articles[2],articles[3],articles[4]


# # BBC

# In[8]:


res = requests.get('https://www.bbc.co.uk/search?q=cryptocurrency',headers=headers)
soup = bs(res.content,'lxml')

articles = [[],[],[],[],[],[]]
x = soup.find(class_='search-results results').find_all('li')
for rawlink in x:
    link = rawlink.find('a').get('href')
    if link not in set(oldlinks):
        try:
            articlesoup = bs(requests.get(link).text, 'html.parser')
            articletext = articlesoup.find('div',class_='story-body__inner')
            articletext.figure.decompose()
            articletext.div.decompose()
            articletext=articletext.get_text(' ', strip=True)
            wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
            words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
            articles[0].append(articlesoup.find(class_='story-body__h1').get_text())
            articles[1].append(pd.to_datetime(articlesoup.find('div',class_='date date--v2').get('data-datetime')))
            articles[2].append(link)
            articles[3].append(articletext)
            articles[4].append(wordslength)
            articles[5].append(words) ### Use to collect all words splitted already for NLP
        except:
            pass
bbc = pd.DataFrame()
bbc['Title'], bbc['Timestamp'], bbc['Links'], bbc['Text'], bbc['Wordslength']  = articles[0],articles[1],articles[2],articles[3],articles[4]


# # Coinspeaker

# In[9]:


res = requests.get('https://www.coinspeaker.com/',headers=headers)
soup = bs(res.content,'lxml')
articles = [[],[],[],[],[],[]]

x = soup.find('div',id='content').find_all('h3')
for rawlink in x:
    link = rawlink.find('a').get('href')
    if link not in set(oldlinks):
        try:
            articlesoup = bs(requests.get(link).text, 'html.parser')
            articletext = articlesoup.find('div',class_='entry-content').get_text('',strip=True)
            wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
            words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
            articles[0].append(articlesoup.find('h1',class_='entry-title-spotlight').get_text())
            articles[1].append(pd.to_datetime(articlesoup.find(class_='timestamp').get_text().replace('Published on ','').replace(' Updated on','')))
            articles[2].append(link)
            articles[3].append(articletext)
            articles[4].append(wordslength)
            articles[5].append(words)
        except:
            pass
    
Coinspeaker = pd.DataFrame()
Coinspeaker['Title'], Coinspeaker['Timestamp'], Coinspeaker['Links'], Coinspeaker['Text'], Coinspeaker['Wordslength']  = articles[0],articles[1],articles[2],articles[3],articles[4]


# In[10]:


Coinspeaker


# # Techbullion

# In[11]:


res = requests.get('https://www.techbullion.com/?s=cryptocurrency')
soup = bs(res.content,'lxml')
articles = [[],[],[],[],[],[]]
x = soup.find(class_='archive-col-list left relative infinite-content').find_all('li')
for rawlink in x:
    link = rawlink.find('a').get('href')
    if link not in set(oldlinks):
        try:
            articlesoup = bs(requests.get(link).text, 'html.parser')
            articletext = articlesoup.find(id='content-main').get_text('',strip=True)
            wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
            words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
            articles[0].append(articlesoup.find('header').find('h1').get_text())
            articles[1].append(pd.to_datetime(articlesoup.find('time').get('datetime')))
            articles[2].append(link)
            articles[3].append(articletext)
            articles[4].append(wordslength)
            articles[5].append(words) ### Use to collect all words splitted already for NLP
        except:
            pass

Techbullion = pd.DataFrame()
Techbullion['Title'], Techbullion['Timestamp'], Techbullion['Links'], Techbullion['Text'], Techbullion['Wordslength']  = articles[0],articles[1],articles[2],articles[3],articles[4]


# # Dailyfintech

# In[12]:


res = requests.get('https://dailyfintech.com/?s=cryptocurrency')
soup = bs(res.content,'lxml')
articles = [[],[],[],[],[],[]]
x = soup.find('div',id='posts-wrapper').find_all(class_='entry-title')
for rawlink in x:
    link = rawlink.find('a').get('href')
    if link not in set(oldlinks):
        try:
            articlesoup = bs(requests.get(link).text, 'html.parser')
            articletext = articlesoup.find('div',class_='entry-content').get_text('',strip=True)
            wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
            words = re.sub('[^a-z\ \']+', ' ',  articletext).split()

            articles[0].append(articlesoup.find(class_='entry-title').get_text('',strip=True))
            articles[1].append(pd.to_datetime(articlesoup.find('time').get('datetime')))
            articles[2].append(link)
            articles[3].append(articletext)
            articles[4].append(wordslength)
            articles[5].append(words) ### Use to collect all words splitted already for NLP
        except:
            pass
    
Dailyfintech = pd.DataFrame()
Dailyfintech['Title'], Dailyfintech['Timestamp'], Dailyfintech['Links'], Dailyfintech['Text'], Dailyfintech['Wordslength']  = articles[0],articles[1],articles[2],articles[3],articles[4]


# # Breakermag

# In[13]:


res = requests.get('https://breakermag.com/')
soup = bs(res.content,'lxml')

articles = [[],[],[],[],[],[]]
x = soup.find('main').find_all('h2')
for rawlink in x:
    link = rawlink.find('a').get('href')
    if link not in set(oldlinks):        
        try:
            articlesoup = bs(requests.get(link).text, 'html.parser')
           
            articletext = articlesoup.find('article').get_text('',strip=True)
            wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
            words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
            if articlesoup.find(class_='article-poster__title') is not None:
                articles[0].append(articlesoup.find(class_='article-poster__title').get_text('',strip=True)) #Title
            else:
                articles[0].append(articlesoup.find(class_='article-poster-vertical__headline').get_text('',strip=True))
            articles[1].append(pd.to_datetime(articlesoup.find('div',class_='article-poster__posted-date').get_text('',strip=True))) # Time
            articles[2].append(link)#Link
            articles[3].append(articletext)#Text
            articles[4].append(wordslength)
            articles[5].append(words) ### Use to collect all words splitted already for NLP
        except:
            pass

Breakermag = pd.DataFrame()
Breakermag['Title'], Breakermag['Timestamp'], Breakermag['Links'], Breakermag['Text'], Breakermag['Wordslength']  = articles[0],articles[1],articles[2],articles[3],articles[4]


# # Venturebeat
# 

# In[14]:


articles = [[],[],[],[],[],[]]

res = requests.get('https://venturebeat.com/?s=cryptocurrency')
soup = bs(res.content,'lxml')
x = soup.find_all('article')
for rawlink in x:
        link = rawlink.find('a').get('href')
        if link not in set(oldlinks):   
            try:
                articlesoup = bs(requests.get(link).text, 'html.parser')
                
                articletext = articlesoup.find('div',id='content').get_text('',strip=True)
                wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
                words = re.sub('[^a-z\ \']+', ' ',  articletext).split()

                articles[0].append(articlesoup.find(class_='article-title').get_text('',strip=True))
                articles[1].append(pd.to_datetime(articlesoup.find('time').get('datetime'))) # Time
                articles[2].append(link)#Link
                articles[3].append(articletext)#Text
                articles[4].append(wordslength)
                articles[5].append(words) ### Use to collect all words splitted already for NLP
            except:
                pass

                
Venturebeat = pd.DataFrame()
Venturebeat['Title'], Venturebeat['Timestamp'], Venturebeat['Links'], Venturebeat['Text'], Venturebeat['Wordslength']  = articles[0],articles[1],articles[2],articles[3],articles[4]


# # Quartz

# In[15]:


articles = [[],[],[],[],[],[]]

url = "https://qz.com/search/cryptocurrency/"

response = requests.get(url, headers)
soup = bs(response.text, "lxml")
x = soup.find(class_='_66ee0 ac70a').find_all('a')
for rawlink in x:
        link = 'https://qz.com' + rawlink.get('href')
        if link not in set(oldlinks):
            try:
                articlesoup = bs(requests.get(link).text, 'html.parser')
                
                articletext = articlesoup.find(class_='f46e3').get_text()        
                wordslength = len(re.sub('[^a-z\ \']+', ' ',  articletext).split())
                words = re.sub('[^a-z\ \']+', ' ',  articletext).split()
                articles[0].append(articlesoup.find('title').get_text())

                articles[1].append(pd.to_datetime(articlesoup.find('time').get('datetime')))
                articles[2].append(link)
                articles[3].append(articletext)
                articles[4].append(wordslength)
                articles[5].append(words) ### Use to collect all words splitted already for NLP
            except:
                pass

qz = pd.DataFrame()
qz['Title'], qz['Timestamp'], qz['Links'], qz['Text'], qz['Wordslength']  = articles[0],pd.to_datetime(articles[1]),articles[2],articles[3],articles[4]


# # Create DataFrame

# In[16]:


def createdf():
    df = livecoinwatch.append([coindesk,forexlive,bbc,cointelegraph,Techbullion,Venturebeat,Dailyfintech,Breakermag,qz,Coinspeaker,cryptocompare],ignore_index = True) 
    df["Timestamp"] = df["Timestamp"].values.astype('datetime64[s]')
    df = df.drop_duplicates(subset = 'Title',keep = 'first')
    df = df.sort_values(by="Timestamp", ascending = False).reset_index(drop=True)
    df = df[["Title","Timestamp","Links","Text","Wordslength"]]
    return df


# In[17]:


dataset = createdf()
dataset.to_json('newscrapednews.json')


# In[ ]:


data

