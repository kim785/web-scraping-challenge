from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():

    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    mars_dict = {}

    # Scrape Mars News Articles
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    time.sleep(1)

    news_html = browser.html
    soup_news = bs(news_html, 'html.parser')

    news_title = soup_news.find_all('div', class_="content_title")[0].text
    news_p = soup_news.find_all('div', class_="article_teaser_body")[0].text

    # Mars Space Images
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    time.sleep(1)

    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    result = image_soup.find_all("img", class_="headerimage fade-in")

    for r in result:
        src = r.get("src")
        featured_image_url = f"{image_url}{src}"

    # Mars Facts
    facts_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(facts_url)
    facts_df = tables[1]
    facts_df.columns = [" ", "Facts"]
    facts_df.set_index(" ", inplace=True)
    table_html = facts_html = facts_df.to_html()
    facts_html = facts_html.replace('\n', '')

    # Mars Hemisphere
    url_hemi = "https://marshemispheres.com/"
    browser.visit(url_hemi)

    time.sleep(1)

    html_hemi = browser.html
    soup_hemi = bs(html_hemi, 'html.parser')

    results_hemi = soup_hemi.find_all('h3')
    results_tag = soup_hemi.find_all('div', class_="description")

    hemisphere_image_urls = []

    for x in range(4):
    
        # Title
        img_title = results_hemi[x].text
    
        # Images
        browser.visit(f"{url_hemi}{results_tag[x].a['href']}")
        html_x = browser.html
        soup_tag = bs(html_x, "html.parser")
        tag = soup_tag.find('img', class_="wide-image").get("src")
        img_url = f"{url_hemi}{tag}"
    
        # Build the dictionary
        post = {}
        post['title'] = img_title
        post['img_url'] = img_url
        hemisphere_image_urls.append(post)
    
    # Build a dictionary for MongoDB
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p
    mars_dict["featured_image_url"] = featured_image_url
    mars_dict["fact_table"] = str(facts_html)
    mars_dict["hemisphere_images"] = hemisphere_image_urls 

    browser.quit()

    return mars_dict