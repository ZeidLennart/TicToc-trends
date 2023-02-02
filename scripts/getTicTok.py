import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

website_HashTags = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
website_Songs = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en"


def WebInteraction(driver, country, number):
    # press dropdown
    selectDropDown = driver.find_element("xpath", '//span[@data-testid="cc_rimless_select_undefined"]')
    selectDropDown.click()

    # search for Germany
    KeyInput = driver.find_element("xpath", '//input[@placeholder="Start typing or select from the list"]')
    KeyInput.send_keys(country);
    time.sleep(2)

    # select Germany
    selectCountry = driver.find_element("xpath", '//div[@data-option-id="SelectOption' + number + '"]')
    selectCountry.click()
    time.sleep(2)

    # select viewMore
    selectViewMore = driver.find_element("xpath", '//div[@data-testid="cc_contentArea_viewmore_btn"]')
    selectViewMore.click()
    time.sleep(2)
    selectViewMore.click()
    time.sleep(2)
    selectViewMore.click()
    time.sleep(2)
    selectViewMore.click()
    time.sleep(2)

def getHashTagData(link, country, number):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)

    # do the interaction with the website
    WebInteraction(driver, country, number)

    # get Data
    rank =[]
    hashtag = []
    post = []
    views = []

    for r in driver.find_elements("xpath", '//span[starts-with(@class,"rankingIndex")]'):
        rank.append(r.text)
    
    for h in driver.find_elements("xpath", '//span[starts-with(@class,"titleText")]'):
        hashtag.append(h.text.replace("k", "000").replace("M", "000000"))
    
    for p in driver.find_elements("xpath", '//div[starts-with(@class,"pav-wrapper")]/div[1]/span[1]'):
        post.append(p.text.replace("k", "000").replace("M", "000000"))

    for v in driver.find_elements("xpath", '//div[starts-with(@class,"pav-wrapper")]/div[2]/span[1]'):
        views.append(v.text.replace("k", "000").replace("M", "000000"))

    driver.quit()

    #save data
    df = pd.read_csv("./Data/TikToc_Hashtags.csv")

    df2 = pd.DataFrame({
        "rank": rank,
        "hashtag": hashtag,
        "posts": post,
        "views": views,
        "country": country,
        "day": datetime.now().date(),
        "timeScriptWasExecuted": datetime.now().time()
        })

    df = pd.concat([df, df2])

    df.to_csv('./Data/TikToc_Hashtags.csv', index=False)

def getSongData(link, country, number):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)
    # do the interaction with the website
    WebInteraction(driver, country, number)

    # get Data
    rank =[]
    name = []
    artist = []
    ImgLink = []

    for r in driver.find_elements("xpath", '//span[starts-with(@class,"rankingIndex")]'):
        rank.append(r.text)
    
    for n in driver.find_elements("xpath", '//span[starts-with(@class,"music-name")]'):
        name.append(n.text)
    
    for a in driver.find_elements("xpath", '//span[starts-with(@class,"auther-name")]'):
        artist.append(a.text)

    for I in driver.find_elements("xpath", '//img[@loading="lazy"]'):
        ImgLink.append(I.get_attribute("src"))

    driver.quit()

    #save data
    df = pd.read_csv("./Data/TikToc_Songs.csv")

    df2 = pd.DataFrame({
        "rank": rank,
        "name": name,
        "artist": artist,
        "ImgLink": ImgLink,
        "country": country,
        "day": datetime.now().date(),
        "timeScriptWasExecuted": datetime.now().time()
        })

    df = pd.concat([df, df2])

    df.to_csv('./Data/TikToc_Songs.csv', index=False)

def harvestData():
    # Harvest Hashtags
    getHashTagData(website_HashTags, "All regions", "6")
    getHashTagData(website_HashTags, "United States", "76")
    getHashTagData(website_HashTags, "Germany", "27")
    getHashTagData(website_HashTags, "United Kingdom", "75")
    getHashTagData(website_HashTags, "Australia", "8")

    # Harvest Songs
    getSongData(website_Songs, "United States", "75")
    getSongData(website_Songs, "Germany", "26")
    getSongData(website_Songs, "United Kingdom", "74")
    getSongData(website_Songs, "Australia", "7")

harvestData()
