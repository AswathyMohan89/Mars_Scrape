import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape1():
    mars_dict={}
    try:
        nasa_list=[]
        nasa_url = 'https://mars.nasa.gov/news/'
        executable_path = {'executable_path': 'chromedriver.exe'}
        nasa_browser = init_browser()
        nasa_browser.visit(nasa_url)
        nasa_html = nasa_browser.html
        soup_nasa = BeautifulSoup(nasa_html, 'html.parser')
        pop_url="https://mars.nasa.gov"
        div_nasa=soup_nasa.find_all("div",class_="image_and_description_container")
        div_nasa=div_nasa[:3]
        for each in div_nasa:
            nasa_dict={}
            #div_title_nasa=each.find("div",class_="list_text").find("a").text
            #div_title_nasa=div_nasa.find("div",class_="list_text")
            #anchor_nasa=div_title_nasa.find("a")
            #news_title=anchor_nasa.text
            news_title=each.find("div",class_="list_text").find("a").text
            date_news=each.find("div",class_="list_text").find("div",class_="list_date").text
            details=each.find("div",class_="list_text").find("div",class_="content_title")
            details_a=details.find("a")["href"]
            img_link=each.find("div",class_="list_image").find("img")
            news_paragraph=each.find("div",class_="article_teaser_body").text
            #div_para=each.find("div",class_="article_teaser_body").text
            #print(date_news)
            #div_para=div_nasa.find("div",class_="article_teaser_body")
            #news_paragraph=div_para.text
            #print("#########################################################")
            #print(nasa_url)
            #print(news_title)
            #print(news_paragraph)
            nasa_dict["news"]=news_title
            nasa_dict["news_paragraph"]=news_paragraph
            nasa_dict["date_news"]=date_news
            nasa_dict["img_link"]=pop_url+img_link["src"]
            nasa_dict["details_a"]=pop_url+details_a
            nasa_list.append(nasa_dict)
        mars_dict["nasa"]=nasa_list
        nasa_browser.quit()

    except Exception as e:
        print(e)


#######################################################################
    try:
        browser_jpl = init_browser()
        url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser_jpl.visit(url_jpl)
        print("#########################################################")
        

        print(url_jpl)

        html_jpl = browser_jpl.html
        soup_jpl = BeautifulSoup(html_jpl, 'html.parser')

        footer = soup_jpl.find('footer')
        a_class=footer.find("a")
        image_url=a_class["data-link"]


        #print(image_url)
        browser_jpl.quit()
    except Exception as e:

            print(e)
    ###########################################################################
    new_url_jpl="https://www.jpl.nasa.gov/"+image_url
    #executable_path = {'executable_path': 'chromedriver.exe'}
    browser_new_jpl = init_browser()
    browser_new_jpl.visit(new_url_jpl)
    html_new_jpl = browser_new_jpl.html
    soup_new_jpl = BeautifulSoup(html_new_jpl, 'html.parser')
    fig_jpl=soup_new_jpl.find("figure", class_="lede")
    anchor_jpl=fig_jpl.find("img")

    featured_image_url="https://www.jpl.nasa.gov"+anchor_jpl["src"]
    print("#########################################################")
    print(new_url_jpl)
    #print(featured_image_url)
    mars_dict["featured_image_url"]=featured_image_url

    browser_new_jpl.quit()
    ###############################################################################
    twitter="https://twitter.com/marswxreport?lang=en"
    #executable_path = {'executable_path': 'chromedriver.exe'}
    twitter_browser = init_browser()
    twitter_browser.visit(twitter)
    twitter_html = twitter_browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')
    #t_list=soup.findAll("div",class_="js-tweet-text-container")

    twitter_list=twitter_soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather=twitter_list.text
    print("#########################################################")
    print(twitter)
    #print(mars_weather)
    mars_dict["mars_weather"]=mars_weather
    twitter_browser.quit()
    ##################################################################################
    import pandas as pd
    facts="http://space-facts.com/mars/"
    
    mars_df=pd.read_html(facts)
    mars_df[0]=mars_df[0].rename(columns={0: 'Description', 1: 'Values'})
    mars_df=mars_df[0]
    mars_df=mars_df.set_index("Description")
    #mars_df.to_html('filename.html')
    mars_df1=mars_df.to_html()
    print("#########################################################")
    mars_dict["facts"]=mars_df1
    #print(mars_df)
    
    ####################################################################################
    hem_list=[]
    hemisphere_list=["cerberus_enhanced","schiaparelli_enhanced","syrtis_major_enhanced","valles_marineris_enhanced"]
    for hem in hemisphere_list:
        hem_dict={}
        hemisphere="https://astrogeology.usgs.gov/search/map/Mars/Viking/"+hem
        executable_path = {'executable_path': 'chromedriver.exe'}
        hem_browser = init_browser()
        hem_browser.visit(hemisphere)
        hem_html = hem_browser.html
        hem_soup = BeautifulSoup(hem_html, 'html.parser')
        div_hem=hem_soup.find("div",class_="downloads")
        img_hem=div_hem.find("a")
        hem_dict["title"]=hem
        hem_dict["image_url"]=img_hem["href"]
        hem_list.append(hem_dict)
        #print(hem + " done")
        #print("https://astrogeology.usgs.gov"+img["src"])
        #https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg
        hem_browser.quit()
    #print(hem_dict)
    #print("****************************************************")
    #print(hem_list)
    mars_dict["hemisphere"]=hem_list

    return mars_dict




