import pickle
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from html import unescape
import random
import time
import re
from youtubeConstant import youtubeConstant as CONT
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from ulties import writeLogWithName
import json
import requests
import re
from ulties import getRealNumber
from selenium.webdriver.common.keys import Keys
from telegram.ext import CallbackContext, JobQueue

mMessage = ''
def sendMessagetoTelegramJob(context: CallbackContext):
    global mMessage
    context.bot.send_message(chat_id='-688061480', 
                             text=mMessage)
def sendMessageToTelegram(message, mJobTelegram: JobQueue):
    global mMessage
    mMessage = message
    mJobTelegram.run_once(sendMessagetoTelegramJob,1)

# seed random number generator
random.seed(time.perf_counter())

def getRandomTime():
    wait = random.randint(30, 60)
    print("random time:{}".format(wait))
    return wait

def getShortRandomTime():
    wait = random.randint(5, 10)
    print("random time:{}".format(wait))
    return wait

def scroll_shim(passed_in_driver, object):  # scroll to element
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)

def cleanhtml(raw_html):
    replaceString = re.sub('<br\s*?>', '\n', raw_html)
    cleantext = BeautifulSoup(replaceString, "lxml").text
    # cleantext = BeautifulSoup(raw_html, "html.parser").text
    return cleantext

class extraData:
    follower = 0
    like = 0
    follow = 0
    extra_info = ["Eve", "Alice", "Bob"]


class youtubeProfile:    
    name = ''
    avatar = ''
    cover = ''
    extra_data = extraData()

    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getInfoYoutube(driver, link, idYoutubePost, idProfile, mJobTelegram: JobQueue):    

    try:
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        logFileName = 'Log/LogInsYoutubeProfile-{}.txt'.format(current_date)

        driver.get(link)
        writeLogWithName(logFileName,'Link: {}'.format(link))            
        time.sleep(getRandomTime())        

        try:
            elementAbout = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, CONT.xpathAbout)))
            scroll_shim(driver,elementAbout)
            time.sleep(2)
            action = ActionChains(driver)
            action.move_to_element(elementAbout).click(elementAbout).perform()
            
            dataUpload = youtubeProfile()
            try:
                elementName = driver.find_element_by_xpath(CONT.xpathName)
                name = elementName.get_attribute('innerHTML')            
                dataUpload.name = name
            except Exception as ex:
                writeLogWithName(logFileName,"Error get name: {}".format(ex))
                dataUpload.name = ''

            try:
                elementImage = driver.find_element_by_xpath(CONT.xpathImage)
                image = elementImage.get_attribute('src')            
                dataUpload.avatar = image
            except Exception as ex:            
                writeLogWithName(logFileName,"Error get image: {}".format(ex))
                dataUpload.avatar = ''

            try:
                elementCover = driver.find_element_by_xpath(CONT.xpathCover)
                cover = elementCover.value_of_css_property('--yt-channel-banner')
                start = cover.find('url("')
                end = cover.find('")')
                cover = cover[start + 5:end]
                if(len(cover) > 5):
                    dataUpload.cover = cover
                else:
                    dataUpload.cover = 'Do not have banner'    
            except Exception as ex:            
                writeLogWithName(logFileName,"Error get cover image: {}".format(ex))
                dataUpload.cover = 'Can not get banner'

            extra = extraData()
            extra.follow = 0
            extra.follower = 0
            extra.like = 0
            infors = ['description']

            try:
                elementSubscriber = driver.find_element_by_xpath(CONT.xpathSubscriber)
                subscriber = elementSubscriber.get_attribute('innerHTML')
                print('subscriber: {}'.format(subscriber))
                subscriberInt = re.sub(r'[^0-9kmKM.,]',r'',subscriber)
                if(len(subscriberInt) > 0):
                    extra.follower = getRealNumber(subscriber)
            except Exception as ex:
                writeLogWithName(logFileName,"Error get subscriber: {}".format(ex))

            try:        
                elementDescription = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, CONT.xpathDescription)))
                description = elementDescription.get_attribute('innerHTML')
                description = cleanhtml(description)            
                infors.append(description)
            except Exception as ex:            
                writeLogWithName(logFileName,"Error get description: {}".format(ex))

            extra.extra_info = infors
            dataUpload.extra_data = extra            
            uploadYoutubeInfo(dataUpload, idProfile, logFileName, mJobTelegram, link)

            #try to get 10 posts
            getPosts(driver,idYoutubePost, idProfile,logFileName)
            
        except Exception as ex:        
            writeLogWithName(logFileName,"Error while get youtube info: {}".format(ex))
    except Exception as ex:
        writeLogWithName(logFileName,"Error catch all: {}".format(ex))
        sendMessageToTelegram("Error catch all: {}".format(ex), mJobTelegram)

def uploadYoutubeInfo(data:youtubeProfile, idYoutube, logFileName, mJobTelegram: JobQueue, link):
    api_url_post = "http://42.119.111.90:8080/crawl/influencer/{}/youtube".format(idYoutube)
    headers =  {"Content-Type":"application/json"}
    responsePost = requests.post(api_url_post, json=data.toJson(), headers=headers)    
    writeLogWithName(logFileName,'Json response post:{}'.format(responsePost.json()))
    writeLogWithName(logFileName,'Status response:{}'.format(responsePost.status_code))
    if(responsePost.status_code != 200):
        sendMessageToTelegram("Error upload profile youtube {}".format(link), mJobTelegram)

class DataPost:
    object_id = ''
    post_time = ''
    platform_code = ''
    influencer_id = ''
    influencer_platform_id = ''
    link = ''
    content = ''
    content_type = 'video'#photo,video,album,gif,livestream,story
    image = []
    video = []
    like = ''
    share = ''
    comment = ''
    view = ''
    tags = []

    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getPosts(driver,idYoutubePost, idProfile, logFileName):    
    time.sleep(getShortRandomTime())
    try:
        elementAbout = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.xpathAllVideo)))
        scroll_shim(driver,elementAbout)
        time.sleep(2)
        action = ActionChains(driver)
        action.move_to_element(elementAbout).click(elementAbout).perform()

        elementVideos = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, CONT.xpathVideos)))

        count = 0        
        for elementVideo in elementVideos:
            count = count + 1
            if(count > 10):
                break
            scroll_shim(driver,elementVideo)
            time.sleep(getShortRandomTime())
            dataPost = DataPost()
            dataPost.influencer_id = idYoutubePost
            dataPost.influencer_platform_id = idProfile
            dataPost.platform_code = 'youtube'
            dataPost.video = []
            dataPost.share = '0'
            imageData = []            
            try:
                imageElement = elementVideo.find_element(By.XPATH,".//yt-img-shadow/img")
                imageDataValue = imageElement.get_attribute('src')
                imageData.append(imageDataValue)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get image:{}'.format(ex))
            dataPost.image = imageData

            try:
                linkElement = elementVideo.find_element(By.XPATH,".//a[@id='thumbnail' and @href]")
                linkValue = linkElement.get_attribute('href')
                dataPost.link = linkValue

                #try to get id                
                idSplit = linkValue.split('=')
                dataPost.object_id = idSplit[len(idSplit)-1]
            except Exception as ex:
                writeLogWithName(logFileName,'Error get link:{}'.format(ex))

            try:
                contentElement = elementVideo.find_element(By.XPATH,".//div[@id='details']//*[@id='video-title']")
                contentValue = contentElement.get_attribute('innerHTML')
                contentValue = cleanhtml(contentValue)
                dataPost.content = contentValue
            except Exception as ex:
                writeLogWithName(logFileName,'Error get content:{}'.format(ex))
                dataPost.content = 'Error get content'

            #try to get time
            try:
                timeElement = elementVideo.find_element(By.XPATH,".//div[@id='metadata-line']/span[2]")
                timeValue = timeElement.get_attribute('innerHTML')
                dataPost.post_time = timeValue
            except Exception as ex:
                writeLogWithName(logFileName,'Error get time first:{}'.format(ex))

            action = ActionChains(driver)            
            action.move_to_element(elementVideo).key_down(Keys.CONTROL).click(elementVideo).key_up(Keys.CONTROL).perform()

            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)
            
            try:
                timeElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, CONT.xpathTime)))
                timeValue = timeElement.get_attribute('innerHTML')
                dataPost.post_time = timeValue
            except Exception as ex:
                writeLogWithName(logFileName,'Error get time:{}'.format(ex))

            try:               
                viewElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, CONT.xpathView)))
                viewValue = viewElement.get_attribute('innerHTML')
                dataPost.view = getRealNumber(cleanhtml(viewValue))
            except Exception as ex:
                writeLogWithName(logFileName,'Error get view:{}'.format(ex))    

            try:
                likeElement = driver.find_element(By.XPATH,'//ytd-video-primary-info-renderer//ytd-menu-renderer//yt-formatted-string[contains(@aria-label,"likes")]')
                likeValue = likeElement.get_attribute('innerHTML')                
                dataPost.like = getRealNumber(likeValue)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get like:{}'.format(ex))
                dataPost.like = '0'

            try:
                commentElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, CONT.xpathComment)))
                commentValue = commentElement.get_attribute('innerHTML')                
                dataPost.comment = getRealNumber(commentValue)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get comment:{}'.format(ex))
                dataPost.comment = '0'

            #get hashtag
            dataHasgTag = []
            try:
                hashTagElements = driver.find_elements_by_xpath(CONT.xpathHashTag)
                for hashTagElement in hashTagElements:
                    hashtag = hashTagElement.get_attribute('innerHTML')
                    hashtag = cleanhtml(hashtag)
                    dataHasgTag.append(hashtag)
                    print('hashtag:{}'.format(hashtag))                    
                dataPost.tags = dataHasgTag  
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get hashtag:{}'.format(ex))

            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

            uploadDataPost(dataPost, logFileName)            

    except Exception as ex:
        print('Error while get post:{}'.format(ex))

def uploadDataPost(data:DataPost, logFileName):
    api_url_post = "http://42.119.111.90:8080/crawl/post"
    headers =  {"Content-Type":"application/json"}
    responsePost = requests.post(api_url_post, json=data.toJson(), headers=headers)    
    writeLogWithName(logFileName,'Json response post:{}'.format(responsePost.json()))
    writeLogWithName(logFileName,'Status response:{}'.format(responsePost.status_code))

def getPostDetail(driver, linkPost):
    try:            
        driver.get(linkPost)            
    except Exception as ex:
        time.sleep(3)
        driver.get(linkPost)

    # testt
    # time.sleep(getRando
    # mTime())
    time.sleep(5)

    try:
        try:
            timeElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, CONT.xpathTime)))
            timeValue = timeElement.get_attribute('innerHTML')      
            print('timeValue:{}'.format(timeValue))
        except Exception as ex:
            print("Error get time:{}".format(ex))

        try:               
            viewElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, CONT.xpathView)))
            viewValue = viewElement.get_attribute('innerHTML')
            print('viewValue:{}'.format(viewValue))            
        except Exception as ex:
            print("Error get view:{}".format(ex))

        try:
            likeElement = driver.find_element(By.XPATH,'//ytd-video-primary-info-renderer//ytd-menu-renderer//yt-formatted-string[contains(@aria-label,"likes")]')
            likeValue = likeElement.get_attribute('innerHTML')    
            print('likeValue:{}'.format(likeValue))                                    
        except Exception as ex:
            print("Error get like:{}".format(ex))

        try:
            commentElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, CONT.xpathComment)))
            commentValue = commentElement.get_attribute('innerHTML')
            print('commentValue:{}'.format(commentValue))        
        except Exception as ex:
            print("Error get comment:{}".format(ex))

            #get hashtag
        dataHasgTag = []
        try:
            hashTagElements = driver.find_elements_by_xpath(CONT.xpathHashTag)
            for hashTagElement in hashTagElements:
                hashtag = hashTagElement.get_attribute('innerHTML')
                hashtag = cleanhtml(hashtag)
                dataHasgTag.append(hashtag)
                print('hashtag:{}'.format(hashtag))                                
        except Exception as ex:                
            print("Error get hashtag:{}".format(ex))

    except Exception as ex:
        print("Error get post:{}".format(ex))

