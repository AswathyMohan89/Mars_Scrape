#import dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import pandas as pd
#define function that initializes browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

#function used to scrape the url
def scrape1():
    #create an empty dictionary to return back for mongodb
    mars_dict={}
###############Scrape Nasa##############################
    try:
        #create an empty list
        nasa_list=[]
        #set the url
        nasa_url = 'https://mars.nasa.gov/news/'
        #set the executable chromdriver path
        executable_path = {'executable_path': 'chromedriver.exe'}
        #call the init_browser() to initialize browser
        nasa_browser = init_browser()
        #visit the specified url
        nasa_browser.visit(nasa_url)
        #retrieve the html for the url
        nasa_html = nasa_browser.html
        #scrape html using soup
        soup_nasa = BeautifulSoup(nasa_html, 'html.parser')
        #set the url for appending the image and anchor tags, so that full urls are made
        pop_url="https://mars.nasa.gov"
        #for all news tags in the soup
        div_nasa=soup_nasa.find_all("div",class_="image_and_description_container")
        #only retrieve latest 3 news
        div_nasa=div_nasa[:3]
        #for each news repeat
        for each in div_nasa:
            #create a dictionary foe each news
            nasa_dict={}
            #retrieve the required fields
            news_title=each.find("div",class_="list_text").find("a").text
            date_news=each.find("div",class_="list_text").find("div",class_="list_date").text
            details=each.find("div",class_="list_text").find("div",class_="content_title")
            details_a=details.find("a")["href"]
            img_link=each.find("div",class_="list_image").find("img")
            news_paragraph=each.find("div",class_="article_teaser_body").text
            #append everything to list
            nasa_dict["news"]=news_title
            nasa_dict["news_paragraph"]=news_paragraph
            nasa_dict["date_news"]=date_news
            nasa_dict["img_link"]=pop_url+img_link["src"]
            nasa_dict["details_a"]=pop_url+details_a
            nasa_list.append(nasa_dict)
        #set dictionary value for news as scraped data
        mars_dict["nasa"]=nasa_list
        #quit the browser
        nasa_browser.quit()
    #handle any exceptions
    except Exception as e:
        print(e)


###############Scrape JPL##################################################################################
    try:
        #Set executable path and initialize browser
        browser_jpl = init_browser()
        url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        #visit url and scrape
        browser_jpl.visit(url_jpl)
        html_jpl = browser_jpl.html
        soup_jpl = BeautifulSoup(html_jpl, 'html.parser')
        #retrieve footer data for url to next page
        footer = soup_jpl.find('footer')
        a_class=footer.find("a")
        image_url=a_class["data-link"]
        #quit browser
        browser_jpl.quit()
    #handle exception
    except Exception as e:

            print(e)
    ####################scrape JPL image using url from JPL################################################
    #set the next image url and scrape data
    new_url_jpl="https://www.jpl.nasa.gov/"+image_url
    browser_new_jpl = init_browser()
    browser_new_jpl.visit(new_url_jpl)
    html_new_jpl = browser_new_jpl.html
    soup_new_jpl = BeautifulSoup(html_new_jpl, 'html.parser')
    fig_jpl=soup_new_jpl.find("figure", class_="lede")
    anchor_jpl=fig_jpl.find("img")
    #set the image url to dictionary
    featured_image_url="https://www.jpl.nasa.gov"+anchor_jpl["src"]
    mars_dict["featured_image_url"]=featured_image_url
    #quit browser
    browser_new_jpl.quit()
######################Scrape twitter for Weather###########################################
    #set url
    twitter="https://twitter.com/marswxreport?lang=en"
    #Set executable path and initialize browser, scrape html
    twitter_browser = init_browser()
    twitter_browser.visit(twitter)
    twitter_html = twitter_browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')
    #scrape weather data from twitter

    twitter_list=twitter_soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather=twitter_list.text
    #set weather data to dictionary
    mars_dict["mars_weather"]=mars_weather
    #quit browser
    twitter_browser.quit()
######################Scrape Facts url for facts###########################################
    #set url
    facts="http://space-facts.com/mars/"
    #read html based using pandas. Since using pandas no need of splinter
    mars_df=pd.read_html(facts)
    #rearrange and clean the table needed
    mars_df[0]=mars_df[0].rename(columns={0: 'Description', 1: 'Values'})
    mars_df=mars_df[0]
    #set index for table
    mars_df=mars_df.set_index("Description")
    #convert the scraped and cleaned data to variable
    mars_df1=mars_df.to_html()
    
    #set it to dictionary
    mars_dict["facts"]=mars_df1
   
    
######################Scrape Astrogeology for mars Hemispheres###########################################   
    #initialize the hem_list for appending hemisphere url 
    hem_list=[]
    #create a list of hemisphere urls
    hemisphere_list=["cerberus_enhanced","schiaparelli_enhanced","syrtis_major_enhanced","valles_marineris_enhanced"]
    #for each hemisphere urls do
    for hem in hemisphere_list:
        #create a dictionary for storing hemisphere details
        hem_dict={}
        #set url
        hemisphere="https://astrogeology.usgs.gov/search/map/Mars/Viking/"+hem
        #Set executable path and initialize browser
        executable_path = {'executable_path': 'chromedriver.exe'}
        hem_browser = init_browser()
        #visit url and get html
        hem_browser.visit(hemisphere)
        hem_html = hem_browser.html
        #scrape html using beautiful soup
        hem_soup = BeautifulSoup(hem_html, 'html.parser')
        #retrieve required fields
        div_hem=hem_soup.find("div",class_="downloads")
        img_hem=div_hem.find("a")
        #set values to dictionary
        hem_dict["title"]=hem_soup.find("h2",class_="title").text
        hem_dict["image_url"]=img_hem["href"]
        #append everything to list
        hem_list.append(hem_dict)
        #quit browser
        hem_browser.quit()
    #set dictionary values
    mars_dict["hemisphere"]=hem_list
    #return dictionary to app.py as object for mongodb
    return mars_dict




