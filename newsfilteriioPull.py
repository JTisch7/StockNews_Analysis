# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 10:59:14 2020

@author: Jonathan
"""

# Package used to execute HTTP POST request to the API
import json
import urllib.request
import pandas as pd
import time
import pytz
from dateutil.parser import parse


def newsFilterPull(frm, ticker, company, begin, end):
    # API endpoint
    API_KEY = 'udeobph0hvgkjaog5lk2adenzaaxko9sjfzipssiw4ikdejirhtiebeibraozeof'
    API_ENDPOINT = "https://api.newsfilter.io/public/actions?token={}".format(API_KEY)
    
    # Define the filter parameters
    #queryString = "(title:AAPL OR description:AAPL OR symbols:AAPL) AND publishedAt:["+str(begin)+" TO "+str(end)+"]"
    queryString = "(title:"+str(company)+" OR title:"+str(ticker)+") AND publishedAt:["+str(begin)+" TO "+str(end)+"]"
    payload = {
        "type": "filterArticles",
        "queryString": queryString,
        "from": frm,
        "size": 50
        }
    
    # Format your payload to JSON bytes
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')
    # Instantiate the request
    req = urllib.request.Request(API_ENDPOINT)
    # Set the correct HTTP header: Content-Type = application/json
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    # Set the correct length of your request
    req.add_header('Content-Length', len(jsondataasbytes))
    # Send the request to the API
    response = urllib.request.urlopen(req, jsondataasbytes)
    # Read the response
    res_body = response.read()
    # Transform the response into JSON
    articles = json.loads(res_body.decode("utf-8"))
    return articles

def createDateframe(frm, ticker, company, begin, end):
    start_time = time.time()
    date = []
    title = []
    desc = []
    source = []

    def loopingFunc(frm, ticker, company, begin, end):
        y = frm + 1
        while frm < y:
            time.sleep(2)
            print('running - slowly but surely : ', frm)
            articles = newsFilterPull(frm=frm, ticker=ticker, company=company, begin=begin, end=end)
            l = 0
            while l < len(articles['articles']):
                title.append(articles['articles'][l]['title'])
                date.append(articles['articles'][l]['publishedAt'])
                source.append(articles['articles'][l]['source']['name'])
                try:
                    desc.append(articles['articles'][l]['description'])
                except:
                    desc.append('')
                l+=1
            y = articles['total']['value']
            frm += 50
            if (frm >= y) and (articles['total']['relation'] == 'gte'):
                timestampStr = parse(date[-1]).strftime("%Y-%m-%d")
                loopingFunc(frm=0, ticker=ticker, company=company, begin=begin, end=timestampStr)
            

    loopingFunc(frm=frm,ticker=ticker,company=company,begin=begin,end=end)
        
    df = pd.DataFrame()        
    df['date'] = date
    df['title'] = title
    df['description'] = desc
    df['source'] = source
    
    for j in range(len(df)):
        df['date'][j] = parse(df['date'][j]).astimezone(pytz.timezone('America/Los_Angeles'))
     
    end_time = time.time()
    totalTime = (end_time-start_time)/60
    return df, totalTime
    #df.to_csv('news'+str(ticker)+'2yrs.csv')
    
    
df, totalTime = createDateframe(frm=0, ticker='GS', company='Goldman Sachs', begin='2019-03-08', end='2021-03-19')













#tryin different pulls to see what is best fit title/description/symbol and AAPL vs Apple
'''
def newsFilterPull(frm, begin, end):
    # API endpoint
    API_KEY = 'udeobph0hvgkjaog5lk2adenzaaxko9sjfzipssiw4ikdejirhtiebeibraozeof'
    API_ENDPOINT = "https://api.newsfilter.io/public/actions?token={}".format(API_KEY)
    
    # Define the filter parameters
    queryString = "((title:International AND title:Business AND title:Machines) OR title:IBM) AND publishedAt:["+str(begin)+" TO "+str(end)+"]"
    #queryString = "(title:"+str(company)+" OR title:"+str(ticker)+") AND publishedAt:["+str(begin)+" TO "+str(end)+"]"
    payload = {
        "type": "filterArticles",
        "queryString": queryString,
        "from": frm,
        "size": 50
        }
    
    # Format your payload to JSON bytes
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')
    # Instantiate the request
    req = urllib.request.Request(API_ENDPOINT)
    # Set the correct HTTP header: Content-Type = application/json
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    # Set the correct length of your request
    req.add_header('Content-Length', len(jsondataasbytes))
    # Send the request to the API
    response = urllib.request.urlopen(req, jsondataasbytes)
    # Read the response
    res_body = response.read()
    # Transform the response into JSON
    articles = json.loads(res_body.decode("utf-8"))
    return articles



data = newsFilterPull(frm=0, begin='2019-03-08', end='2021-01-29')


data2 = newsFilterPull(frm=0, ticker='AAPL', company='Apple', begin='2020-08-08', end='2021-01-29')
data3 = newsFilterPull(frm=0, begin='2020-08-08', end='2021-01-29')
data4 = newsFilterPull(frm=0, begin='2020-08-08', end='2021-01-29')
data5 = newsFilterPull(frm=0, begin='2020-08-08', end='2021-01-29')
'''