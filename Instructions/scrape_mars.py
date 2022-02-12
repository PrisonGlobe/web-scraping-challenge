# imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# scrape all function
def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    #return json with all of the data to be loaded into MongoDB
    print("Scrape all reached")
    # get info from news page
    news_title, news_paragraph = scrape_news(browser)

    # build a dict with infofrom scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featureImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }


    browser.quit()


    return marsData

# scrape mars news page
def scrape_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

# Optional delay for loading the page
    html = browser.html
    news_soup = soup(html,'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    # grabs title
    news_title = slide_elem.find('div', class_='content_title').get_text()
    #grab paragraph
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()


    #return the title and the paragaph
    return news_title, news_p



# scrape feature image page
def scrape_feature_img(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    featured_image_url = browser.find_by_tag('button')[1]
    featured_image_url.click()  

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #grab image
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # Use `pd.read_html` to pull the data from the Mars-Earth Comparison section
    # hint use index 0 to find the table
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url



# scrape facts page
def scrape_facts_page(browser):
    # Visit URL
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    fact_soup = soup(html, 'html.parser')

    # find the facts location
    facts_location = fact_soup.find('div', class_="diagram mt-4")
    fact_table = facts_location.find('table')

    # create an empty string
    facts = ""

    # add the text to the empty string then return
    facts += str(fact_table)

    return facts

# scrape hemispheres page
def scrape_hemispheres(browser):
    # base url
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # set up the loop
    for i in range(4):
        # loops through each of the pages
        # hemisphere info dictionary
        hemisphere_info = {}
    
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphere_info["img_url"] = sample['href']
    
        # Get Hemisphere title
        hemisphere_info['title'] = browser.find_by_css('h2.title').text
    
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere_info)
    
        # Finally, we navigate backwards
        browser.back()

    # return the hemisphere url with the titles
    return hemisphere_image_urls    


# Set up as a flask app
if __name__ == "__main__":

    print(scrape_all())