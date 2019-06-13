from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path":"/Users/xiening/Downloads/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_data = {}

    nasa_news_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_news_url)

    nasa_news_html = browser.html
    soup = bs(nasa_news_html,"html.parser")

    #scrapping latest news about mars from nasa
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph 
    
    #Mars Featured Image
    nasa_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(nasa_image_url)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_image_url))
    
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    
    #get image url using BeautifulSoup
    image_html = browser.html
    soup = bs(image_html, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    image_url = base_url + img_url
    mars_data["featured_image"] = image_url
    
    # #### Mars Weather

    #get mars weather's latest tweet from the website
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    weather_html = browser.html
    soup = bs(weather_html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = mars_weather

    # #### Mars Facts

    facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(facts_url)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_data["mars_facts_table"] = mars_html_table

    # #### Mars Hemisperes

    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)
    hemis_html = browser.html
    soup = bs(hemis_html, 'html.parser')
    hemisphere_image_urls=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        hemis_html = browser.html
        soup = bs(hemis_html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = hemisphere_image_urls
    # Return the dictionary
    return mars_data