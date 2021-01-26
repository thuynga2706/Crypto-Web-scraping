#!/usr/bin/env python
# coding: utf-8

# In[39]:


#This is for Prediction
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
import datetime as dt
from datetime import timedelta


# In[40]:


olddata=pd.read_json('dataset.json')
newscrapednews = pd.read_json('newscrapednews.json') #all new articles that day


# In[41]:


def vader(df):   
    df['RatingIndex'] = 'abc'
    df['sentiment'] = 'abc'
    for i in range(len(df)):
        compound = analyser.polarity_scores(df['Text'].iloc[i])['compound']
        df['RatingIndex'].iloc[i] = compound    
        if compound<-0.5:
            df['sentiment'].iloc[i] = 'NEGATIVE'
        elif compound > 0.5:
            df['sentiment'].iloc[i] = 'POSITIVE'
        else:
            df['sentiment'].iloc[i] = 'NEUTRAL'
    return df


# In[42]:


vadersdata= vader(newscrapednews)
newdata = vadersdata.append(olddata,ignore_index=True) #add all new articles with sentiments to old dataset
newdata.to_json('dataset.json')


# # Top 20 articles for Marketing team

# In[43]:


vadersdata=vadersdata[vadersdata['Timestamp']>pd.to_datetime(dt.datetime.now() - timedelta(hours=24))]


# In[44]:


postivesentiment = vadersdata[vadersdata["sentiment"]=="POSITIVE"].sort_values(by="RatingIndex", ascending=False).head(10)
negativesentiment= vadersdata[vadersdata["sentiment"]=="NEGATIVE"].sort_values(by="RatingIndex", ascending=False).head(10)
finaloutput = postivesentiment.append(negativesentiment)


# In[13]:


finaloutput.to_excel('NewsSentiment.xlsx')


# In[45]:


finaloutput


# In[ ]:




