import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



website = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
#path = "/usr/local/bin/chromedriver"
#driver = webdriver.Chrome(path)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(website)


def dataForGermany():
    # press dropdown
    selectDropDown = driver.find_element("xpath", '//span[@data-testid="cc_rimless_select_undefined"]')
    selectDropDown.click()

    # search for Germany
    KeyInput = driver.find_element("xpath", '//input[@placeholder="Start typing or select from the list"]')
    KeyInput.send_keys("Germany");
    time.sleep(2)

    # select Germany
    selectCountry = driver.find_element("xpath", '//div[@data-option-id="SelectOption27"]')
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

    # get Data
    charts = driver.find_elements("id", "hashtagItemContainer")
    print(charts)

    rank =[]
    hashtag = []
    post = []
    views = []

    for chart in charts:
        print(chart.find_element("xpath", '//span[starts-with(@class,"titleText")]').text)
        

    driver.quit()

driver.get(website)
dataForGermany()
