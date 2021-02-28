# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


executable_path = {'executable_path': '../chromedriver'}
browser = Browser('chrome', **executable_path)

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

# ## JPL Space Images Featured Image

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

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()