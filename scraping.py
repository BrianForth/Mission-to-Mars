# Import dependencies
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path= "../chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last modified": dt.datetime.now()
    }
    # Stop webdriver, return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Optional delay for loading page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert browser html to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try: 
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # slide_elem.find("div", class_='content_title')
        # Use parent element to find first 'a' tag and save as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use parent element paragraph text
        news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try: 
        # Find relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use base url to create full url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

def mars_facts():
    try:  
        # Scrape table into df
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set df index
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Convert df to html, add bootstrap
    return df.to_html()

def mars_hemispheres(browser):
    try:
        # 1. Use browser to visit the URL 
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        # 2. Create a list to hold the images and titles.
        hemispheres = []

        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        for x in range(0,4):
            # Click on link to get to full res image
            full_image_elem = browser.find_by_tag('h3')[x]
            full_image_elem.click()
            browser.is_element_present_by_css("img", wait_time=1)
    
            # Pull URL for full res image
            img_url = browser.links.find_by_text('Sample').first['href']

            # Parse HTML to find title
            html = browser.html
            img_soup = soup(html, 'html.parser')
            img_title = img_soup.find('h2', class_='title').get_text()
    
            # Append list with new dictionary 
            hemispheres.append({'title': img_title, 'img_url': img_url})
    
            # Return to main page
            browser.visit(url)
    except:
        return None
    # 4. Quit the browser
    browser.quit()

    #5. Return list
    return hemispheres



if __name__ == "__main__":
    # If running as script, print scripted data
    print(scrape_all())