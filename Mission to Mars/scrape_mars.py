from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():

    executable_path = {'executable_path': 'C:\\Users\\jake_\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape_info():
    browser = init_browser()
    mars_data = []
#NEws
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = None
    news_p = None

    try:
        element = soup.select_one('ul.item_list li.slide')
        news_title = element.find('div', class_ = "content_title").get_text()
        news_p = element.find('div', class_ = "article_teaser_body").get_text()
    except:
        pass

#Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    element = browser.find_by_id('full_image')[0]
    element.click()
    browser.is_element_present_by_text('more info', wait_time = 1)
    more_info_element = browser.links.find_by_partial_text('more info')
    more_info_element.click()
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image = None

    try:
        featured_image_rel= soup.select_one('figure.lede a img').get("src")
        new_url = 'https://www.jpl.nasa.gov'
        featured_image = new_url + featured_image_rel
    except:
        pass
#Tables
    table_url = 'https://space-facts.com/mars/'
    time.sleep(2)
    try:
        tables = pd.read_html(table_url)
        print(tables)
        tables.columns=['Descriptions' , 'Info']
        html_table = tables.to_html(index = False)
    except: 
        html_table = None
    #html_table = None


#Hemisphere urls
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup =bs(html, 'html.parser')

    hemispheres = soup.find_all('h3')
    titles = []
    for hemisphere in hemispheres:
        titles.append(hemisphere.text)
    
    hemisphere_image_urls = []
    for title in titles:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_url = soup.find_all('li')[0].a['href']
        
        
        dict1 = {}
        dict1['title'] = title
        dict1['img_url'] = image_url
        hemisphere_image_urls.append(dict1)
    
    mars_data = {
        "news_title" : news_title,
        "news_p" : news_p,
        "feature_url" : featured_image,
        "mars_table": html_table,
        "hemispheres" : hemisphere_image_urls
    }

    browser.quit()

    return mars_data