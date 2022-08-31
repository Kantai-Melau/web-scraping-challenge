from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import pandas as pd


def scrape():
    # Nasa Mars News
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit website
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Collect the latest News Title
    news_title = soup.body.find_all('div', class_='content_title')[0].text

    #Collect the Paragraph Text
    news_p = soup.body.find_all('div', class_='article_teaser_body')[0].text

    #Close the webpage
    browser.quit()

    # Mars Space Image
    #Getting the image url
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    time.sleep(1)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    #Parse the resulting html with soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Find the image url
    featured_image_url = soup.find('img', class_= 'fancybox-image').get('src')

    #Get the full image url
    full_url = url + featured_image_url
    browser.quit()

    #Mars Facts
    #Get the table from the url
    url = 'https://galaxyfacts-mars.com'

    tables = pd.read_html(url)
    #Specify the exact table and store it in a df
    df = tables[0]
    df.head(11)

    #Rename the column headers
    df.rename(columns=df.iloc[0], inplace = True)

    #Drop the repeated 1st row
    new_df = df.drop([0])

    #Reset index
    new_df = new_df.reset_index(drop = True)
    #Convert to a HTML table
    html_table = new_df.to_html()
    html_table.replace('\n', '')

    #Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # First, get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css('h2.title').text
    
    # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
        browser.back()

    mars_data = {
        "news_title": news_title,
        "paragraph": news_p,
        "image_url": full_url,
        "table": html_table,
        "hemisphere_urls": hemisphere_image_urls
    }

    browser.quit()

    #Return results

    return mars_data
   

