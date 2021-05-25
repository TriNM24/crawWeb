from selenium import webdriver
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://khoahoc.tv/")
SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
print("last height {}".format(last_height))
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    height = driver.execute_script("return document.body.scrollHeight")
    print("scroll from 0 to {}".format(height))
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    print("new height {}".format(new_height))
    if new_height == last_height:
        break
    last_height = new_height
# input()
