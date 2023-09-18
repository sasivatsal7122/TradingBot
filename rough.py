#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[25]:


from datetime import datetime, timedelta
import requests
import configparser


# # Reading config file

# In[33]:


config.read('config.ini')

API_KEY = config['Data']['API_KEY']

stocktickers = config['Data']['stockticker'].split(",")
smaWindows = config['Data']['sma window'].split(",")
emaWindows = config['Data']['ema window'].split(",")
timespans = config['Data']['timespan'].split(",")


# In[34]:


print(stocktickers,smaWindows,emaWindows,timespans)


# ## Creating SMA Tuples

# In[40]:


sma_tuples = []

for item1 in stocktickers:
    for item2 in smaWindows:
        for item3 in timespans:
            sma_tuples.append((item1, item2, item3))

for tpl in sma_tuples:
    print(tpl)


# # Creating EMA Tuples

# In[41]:


ema_tuples = []

for item1 in stocktickers:
    for item2 in emaWindows:
        for item3 in timespans:
            ema_tuples.append((item1, item2, item3))

for tpl in ema_tuples:
    print(tpl)


# # Daily Open and Close

# In[28]:


def getOpenandClose(stockTicker):
    current_date = datetime.now()
    day_before = current_date - timedelta(days=1)
    TIMESTAMP = day_before.strftime('%Y-%m-%d')
    res = requests.get(f"https://api.polygon.io/v1/open-close/{stockTicker}/{TIMESTAMP}?adjusted=true&apiKey={API_KEY}")
    return res.json()


# # Simple Moving Average

# In[ ]:


def getSMA(stockTicker,window,timespan):
    

