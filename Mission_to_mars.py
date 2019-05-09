#!/usr/bin/env python
# coding: utf-8

# In[33]:


from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import os
import time
from splinter import Browser
import pandas as pd
import pymongo


# In[34]:

def scrape():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)


      # In[35]:


    db = client.mars_db
    collection = db.hemis


      # In[36]:


    nasa_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


      # In[37]:


      #response=requests.get(url)

      #os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
      #driver = webdriver.Chrome(chromedriver)



      # In[38]:


    driver.get(nasa_url)
    time.sleep(5)
    html=driver.page_source
    soup = bs(html, 'lxml')
    news_title=soup.find("div", class_="content_title").text
    news_p=soup.find("div", class_="article_teaser_body").text

      


      # In[39]:


    executable_path = {'executable_path':'C:/webdriver/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


      # In[40]:


    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)


      # In[41]:



    html2 = browser.html
    soup=bs(html2, "html.parser")

    soup.find("a",class_="button fancybox")
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)
    soup.find("a", class_="button")
    browser.click_link_by_partial_text("more info")

    featured_image_url=soup.a["href"]
    featured_image_url
      

      
      
      


      # In[42]:


    url3="https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html3=browser.html


      # In[43]:


    soup=bs(html3,"html.parser")


      # In[46]:


    mars_weather=soup.find("div", class_="js-tweet-text-container").text


      # In[47]:



    url4="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)


      # In[48]:


    html4=browser.html
    soup=bs(html4,"html.parser")


      # In[49]:


    hemispheres=soup.find_all("div", class_="item")
    for hemisphere in hemispheres:
        title=hemisphere.find("h3").text.strip()
        img_url=hemisphere.a["href"]
        
        posts={"title": title,
               "img_url":img_url
             }
            
    collection.insert_one(posts)


      # In[50]:


      # Display items in MongoDB collection
    listings = db.hemis.find()


      # In[51]:


    url5="https://space-facts.com/mars/"
    tables=pd.read_html(url5)
    df=tables[0]
    html_table=(df.to_html()).replace("n","")


      # In[54]:


    mars_data={"news_title":news_title,
            "news_p":news_p,
      "mars_image":featured_image_url,
      "current_weather":mars_weather,
      "table":html_table,
      "hemisphere_images": listings
            }
    return mars_data


# In[ ]:




