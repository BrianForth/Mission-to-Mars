# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set executable path
executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path)

# ### Visit the NASA Mars News Site
# Visit mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')
slide_elem.find("div", class_='content_title')

# Use parent element to find first 'a' tag and save as 'news_title'
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use parent element paragraph text
news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Images
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use base url to create full url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

# ### Mars Facts
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df.to_html()

browser.quit()

# ### Mars Weather
# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres
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
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # Pull URL for full res image
    img_url = browser.links.find_by_text('Sample').first['href']

    # Parse HTML to find title
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_title = img_soup.find('h2', class_='title').get_text()
    
    # Append list with new dictionary 
    hemispheres.append({'Title': img_title, 'URL': img_url})
    
    # Return to main page
    browser.visit(url)

# 4. Print the list that holds the dictionary of each image url and title.
hemispheres

# 5. Quit the browser
browser.quit()