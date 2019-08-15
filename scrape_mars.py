import pymongo
from flask import Flask, render_template, redirect
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


## NASA Mars News
def title():
    try:
        nasa_news_url = 'https://mars.nasa.gov/news/'
        nasa_news_response = requests.get(nasa_news_url)
        nasa_news_soup = BeautifulSoup(nasa_news_response.text, 'html.parser')
        nasa_news_title = nasa_news_soup.find('div', class_='content_title').find('a').text.strip()
    except AttributeError:
        return None
    return nasa_news_title

def text():
    try:
        nasa_news_url = 'https://mars.nasa.gov/news/'
        nasa_news_response = requests.get(nasa_news_url)
        nasa_news_soup = BeautifulSoup(nasa_news_response.text, 'html.parser')
        nasa_news_text = nasa_news_soup.find('div', class_="rollover_description_inner").text.strip()    
    except AttributeError:
        return None
    return nasa_news_text    



# JPL Mars Space Images
def images():
    try:
        executable_path = {'executable_path': 'chromedriver'}
        space_image_browser = Browser('chrome', **executable_path, headless=False)
        space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        space_image_browser.visit(space_image_url)
        space_image_html = space_image_browser.html
        space_image_soup = BeautifulSoup(space_image_html, 'html.parser')
        space_image = space_image_soup.find('div', class_='carousel_container').article['style']
        space_image_formatted = space_image.replace("background-image: url('",'').replace("');", '')
        jpl_url = 'https://www.jpl.nasa.gov'
        featured_image_url = jpl_url + space_image_formatted
    except AttributeError:
        return None
    space_image_browser.quit()    
    return featured_image_url


# Mars Weather - twitter
def weather():
    try:
        executable_path = {'executable_path': 'chromedriver'}
        twitter_browser = Browser('chrome', **executable_path, headless=False)    
        twitter_url = 'https://twitter.com/marswxreport?lang=en'
        twitter_browser.visit(twitter_url)
        twitter_html = twitter_browser.html
        twitter_soup = BeautifulSoup(twitter_html, 'html.parser')
        mars_weather = twitter_soup.find('div', class_="js-tweet-text-container").find('p').text
    except AttributeError:
        return None
    twitter_browser.quit()    
    return mars_weather


# Mars Facts   
def facts():
    try:
        facts_url = 'https://space-facts.com/mars/'
        mars_facts = pd.read_html(facts_url)[1]
        mars_facts_html = mars_facts.to_html(index=False, header=False, border="0").replace('\n', '')
    except AttributeError:
        return None
    return mars_facts_html


# Hemispheres Images
def hemispheres():
    try:
        executable_path = {'executable_path': 'chromedriver'}
        hemispheres_browser = Browser('chrome', **executable_path, headless=False)     
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        hemispheres_browser.visit(hemispheres_url)
        hemispheres_html = hemispheres_browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemis_titles = hemispheres_soup.find_all('h3')
        dict_keys = []
        for i in hemis_titles:
            dict_keys.append(str(i).replace("<h3>", '').replace("</h3>", ''))

        images_url = 'https://astrogeology.usgs.gov'
        hemispheres_images= hemispheres_soup.find_all('img', class_='thumb')
        dict_values = []

        for result in hemispheres_images:
            dict_values. append(images_url + result['src'])

        hemisphere_image_urls = [{"title": i, "img_url":k} for i, k in zip(dict_keys, dict_values)]
    except AttributeError:
        return None
    hemispheres_browser.quit()
    return hemisphere_image_urls   

def scrape():
    mars_dict = {'title': title(),
                'text': text(),
                'images': images(),
                'weather': weather(),
                'facts': facts(),
                'hemispheres': hemispheres()}            
    return mars_dict

    



