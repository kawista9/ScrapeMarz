#!/usr/bin/env python
# coding: utf-8

# In[59]:


from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import os
import time
from splinter import Browser
import pandas as pd
import pymongo


# In[60]:

def scrape():
  conn = 'mongodb://localhost:27017'
  client = pymongo.MongoClient(conn)


  # In[61]:


  db = client.mars_db
  collection = db.hemis


  # In[62]:


  nasa_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


  # In[63]:


  #response=requests.get(url)

  #os.environ["webdriver.chrome.driver"] = chromedriver
  driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
  #driver = webdriver.Chrome(chromedriver)
  driver.get(nasa_url)
  time.sleep(5)
  driver.page_source


  # In[69]:


  soup = bs(html, 'lxml')
  news_title=soup.find("div", class_="content_title").text
  news_p=soup.find("div", class_="article_teaser_body").text

      


  # In[70]:


  executable_path = {'executable_path':'C:/webdriver/chromedriver.exe'}
  browser = Browser('chrome', **executable_path, headless=False)


  # In[71]:


  url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
  browser.visit(url2)


  # In[72]:


  html2 = browser.html


  # In[73]:


  soup = bs(html2, 'html.parser')
  link = soup.article['style']


  # In[74]:


  start = link.find("/space")
  stop = link.find(".jpg'") + 4
  featured_image_url = link[start:stop]


  # In[75]:


  url3="https://twitter.com/marswxreport?lang=en"
  browser.visit(url3)
  html3=browser.html


  # In[76]:


  soup=bs(html3,"html.parser")


  # In[77]:


  mw=soup.find("div", class_="js-tweet-text-container").text


  # In[78]:


  start=mw.find("sol")
  stop=mw.find(" hPapic")
  mars_weather=mw[start:stop]


  # In[79]:



  url4="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
  browser.visit(url4)


  # In[80]:


  html4=browser.html
  soup=bs(html4,"html.parser")


  # In[84]:


  hemispheres=soup.find_all("div", class_="item")
  for hemisphere in hemispheres:
      title=hemisphere.find("h3").text.strip()
      img_url=hemisphere.a["href"]
      
      
          
      posts={
          "title": title,
          "img_url":img_url
            }
          
      collection.insert_one(posts)


  # In[85]:


  # Display items in MongoDB collection
  listings = db.hemis.find()


  # In[88]:


  url5="https://space-facts.com/mars/"
  tables=pd.read_html(url5)
  df=tables[0]
  html_table=(df.to_html()).replace("n","")

  mars_data={
    "news_title":news_title,
    "news_p":news_p,
    "mars_image":featured_image_url,
    "current_weather":mars_weather,
    "table":html_table,
    "hemisphere_images": listings
  }
  return mars_data