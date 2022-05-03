import pickle
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from html import unescape
import random
import time
import re
from facebookUlties import loginFace
from tiktokConstant import tiktokConstant as CONT
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import requests
import json
from ulties import writeLogWithName
from ulties import getRealNumber
from telegram.ext import CallbackContext, JobQueue

mMessage = ''
def sendMessagetoTelegramJob(context: CallbackContext):
    global mMessage
    context.bot.send_message(chat_id='-704354720', 
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

def manualLoginAndSaveCokies(driver):
    time.sleep(5)
    driver.get('https://www.tiktok.com')
    input("manual verify procress before save cookies")
    # save cookies
    if os.path.exists(CONT.cookies_file):
        os.remove(CONT.cookies_file)
        print('remove file {}'.format(CONT.cookies_file))
    pickle.dump(driver.get_cookies(), open(
    CONT.cookies_file, "wb"))
    print("Login and save cookies success")

class extraData:
    follower = 1
    like = 1
    follow = 1
    extra_info = ["Eve", "Alice", "Bob"]


class TikTokProfile:    
    name = ''
    avatar = ''    
    extra_data = extraData()

    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getInfoTiktok(driver, link, idTiktokPost, idProfile, mJobTelegram: JobQueue):    

    try:
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        logFileName = 'Log/LogTiktokProfile-{}.txt'.format(current_date)
        writeLogWithName(logFileName,'Link :{}'.format(link))        
        driver.get(link)
        
        time.sleep(getRandomTime())
        
        try:        
            try:
                elementCloseVerify = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, CONT.xpathCloseVerify)))
                elementCloseVerify.click()
                print("click close verify")        
            except Exception as ex:
                print("error get close verify: {}".format(ex))

            dataUpload = TikTokProfile()

            try:
                elementName = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, CONT.xpathName)))
                name = elementName.get_attribute('innerHTML')                
                dataUpload.name = cleanhtml(name)
            except Exception as ex:            
                writeLogWithName(logFileName,"Error get name: {}".format(ex))
                dataUpload.name = ''

            try:            
                elementImage = driver.find_element(By.XPATH,CONT.xpathImage)
                image = elementImage.get_attribute('src')
                dataUpload.avatar = image
            except Exception as ex:            
                writeLogWithName(logFileName,"Error get image: {}".format(ex))
                dataUpload.avatar = ''

            extra = extraData()
            extra.follow = 0
            extra.follower = 0
            extra.like = 0
            infors = []
            try:
                elementInfoMain = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, CONT.xpathInfos)))
                elementInfos = elementInfoMain.find_elements(By.XPATH,"./div")
                for elementInfo in elementInfos:
                    info = elementInfo.get_attribute('innerHTML')
                    info = cleanhtml(info)
                    if('Đang Follow' in info or 'Following' in info):
                        # followInt = re.sub(r'[^0-9kmKM.,]',r'',info)
                        extra.follow = getRealNumber(info)
                    if('Follower' in info):
                        # followerInt = re.sub(r'[^0-9kmKM.,]',r'',info)
                        extra.follower = getRealNumber(info)
                    if('Thích' in info or 'Likes' in info):
                        # likeInt = re.sub(r'[^0-9kmKM.,]',r'',info)
                        extra.like = getRealNumber(info)
            except Exception as ex:            
                writeLogWithName(logFileName,"Error get infor: {}".format(ex))

            try:            
                elementDescription = driver.find_element(By.XPATH,CONT.xpathDescription)
                description = elementDescription.get_attribute('innerHTML')
                infors.append(description)
            except Exception as ex:            
                writeLogWithName(logFileName,"Error get description: {}".format(ex))                

            extra.extra_info = infors
            dataUpload.extra_data = extra            
            uploadTiktokInfo(dataUpload, idProfile, logFileName, mJobTelegram, link)

            getPosts(driver,idTiktokPost, idProfile,logFileName)

        except Exception as ex:        
            writeLogWithName(logFileName,'Error while get tiktok info: {}'.format(ex))
    except Exception as ex:
        writeLogWithName(logFileName,"Error catch all: {}".format(ex))
        sendMessageToTelegram("Error catch all: {}".format(ex), mJobTelegram)

def uploadTiktokInfo(data:TikTokProfile, idTiktok, logFileName, mJobTelegram: JobQueue, link):
    api_url_post = "http://42.119.111.90:8080/crawl/influencer/{}/tiktok".format(idTiktok)
    headers =  {"Content-Type":"application/json"}
    responsePost = requests.post(api_url_post, json=data.toJson(), headers=headers)    
    writeLogWithName(logFileName,'Json response post:{}'.format(responsePost.json()))
    writeLogWithName(logFileName,'Status response:{}'.format(responsePost.status_code))
    if(responsePost.status_code != 200):
        sendMessageToTelegram("Error upload profile tiktok {}".format(link), mJobTelegram)

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
    view = 0
    tags = []

    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getPosts(driver,idTiktokPost, idProfile, logFileName):    
    time.sleep(getShortRandomTime())    
    try:
        elementPosts = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, CONT.xpathVideos)))
        count = 0        
        for elementPost in elementPosts:
            count = count + 1
            if(count > 10):
                break

            time.sleep(getShortRandomTime())            

            dataPost = DataPost()
            dataPost.influencer_id = idTiktokPost
            dataPost.influencer_platform_id = idProfile
            dataPost.platform_code = 'tiktok'
            dataPost.video = []
            dataPost.image = []
            dataPost.share = '0'
            dataPost.view = 0
            videoData = []
            imageData = []

            try:                
                imageElement = WebDriverWait(elementPost, 10).until(EC.presence_of_element_located((By.XPATH,".//img")))                
                imageValue = imageElement.get_attribute('src')
                # start = imageValue.find('url("')
                # end = imageValue.find('")')
                # imageValue = imageValue[start + 5:end]
                imageData.append(imageValue)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get video:{}'.format(ex))
            dataPost.image = imageData

            try:
                viewElement = elementPost.find_element(By.XPATH,'.//*[contains(@class,"video-count")]')
                viewValue = viewElement.get_attribute('innerHTML')
                dataPost.view = getRealNumber(viewValue)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get view:{}'.format(ex))         

            #click to get detail
            scroll_shim(driver,elementPost)
            time.sleep(2)
            action = ActionChains(driver)
            action.move_to_element(elementPost).click(elementPost).perform()

            try:
                elementContent = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"video-infos-container")]//*[contains(@class,"video-meta-title")] | //body//div[@data-e2e="browse-video-desc"]')))
                contentValue = elementContent.get_attribute('innerHTML')
                contentValue = cleanhtml(contentValue)
                dataPost.content = contentValue
            except Exception as ex:
                writeLogWithName(logFileName,'Error get content:{}'.format(ex))

            #get hashtag
            dataHasgTag = []
            try:
                hashTagElements = driver.find_elements_by_xpath('//body//div[contains(@class,"MainContent")]//a[contains(@href,"tag")]')
                for hashTagElement in hashTagElements:
                    hashtag = hashTagElement.get_attribute('innerHTML')
                    hashtag = cleanhtml(hashtag)
                    dataHasgTag.append(hashtag)                    
                dataPost.tags = dataHasgTag
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get hashtag:{}'.format(ex))

            try:
                videoElement = driver.find_element(By.XPATH,"//video[@src]")
                videoValue = videoElement.get_attribute('src')
                videoData.append(videoValue)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get video:{}'.format(ex))
            dataPost.video = videoData

            try:
                linkElement = driver.find_element(By.XPATH,'//body//p[@data-e2e="browse-video-link"]')
                linkValue = linkElement.get_attribute('innerHTML')
                dataPost.link = linkValue

                #try to get id                
                idSplit = linkValue.split('?')                
                idSplit = idSplit[0].split('/')
                dataPost.object_id = idSplit[len(idSplit)-1]                
            except Exception as ex:
                writeLogWithName(logFileName,'Error get link:{}'.format(ex))    

            try:
                timeElement = driver.find_element(By.XPATH,'//div[contains(@class,"InfoContainer")]//*[@data-e2e="browser-nickname"]')
                timeValue = timeElement.get_attribute('innerHTML')
                dataPost.post_time = cleanhtml(timeValue)            
            except Exception as ex:
                writeLogWithName(logFileName,'Error get time:{}'.format(ex))   

            try:
                likeElement = driver.find_element(By.XPATH,'//*[@data-e2e="browse-like-count"]')
                likeValue = likeElement.get_attribute('innerHTML')
                dataPost.like = getRealNumber(likeValue)                    
            except Exception as ex:
                writeLogWithName(logFileName,'Error get like:{}'.format(ex))
                dataPost.like = 0

            try:
                commentElement = driver.find_element(By.XPATH,'//*[@data-e2e="browse-comment-count"]')
                commentValue = commentElement.get_attribute('innerHTML')
                dataPost.comment = getRealNumber(commentValue)                    
            except Exception as ex:
                writeLogWithName(logFileName,'Error get comment:{}'.format(ex))
                dataPost.comment = 0

            uploadDataPost(dataPost,logFileName)

            #try to close detail
            try:
                elementCloseVerify = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, CONT.xpathCloseVerify)))
                elementCloseVerify.click()
                print("click close verify")        
            except Exception as ex:
                print("error get close verify: {}".format(ex))

            time.sleep(2)

            try:
                closeElement = driver.find_element(By.XPATH,'//button[@data-e2e="browse-close"]')
                action = ActionChains(driver)
                action.move_to_element(closeElement).click(closeElement).perform()                 
            except Exception as ex:
                writeLogWithName(logFileName,'Error click cloase:{}'.format(ex))


    except Exception as ex:
        writeLogWithName(logFileName,'Error get posts:{}'.format(ex))

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
    #try to close verify
    try:
        elementCloseVerify = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, CONT.xpathCloseVerify)))
        elementCloseVerify.click()
        print("click close verify")        
    except Exception as ex:
        print("error get close verify: {}".format(ex))

    try:
        postElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-e2e="recommend-list-item-container"][1]')))
        
        # try to get image
        try:
            imageElement = postElement.find_element(By.XPATH,'.//div[@data-e2e="feed-video"]//img')
            image = imageElement.get_attribute('src')
            print("image:{}".format(image))
        except Exception as ex:
            print("Error get image:{}".format(ex))    

        #try to get like
        try:
            likeElement = postElement.find_element(By.XPATH,'.//*[@data-e2e="like-count"]')
            like = likeElement.get_attribute('innerHTML')
            like = getRealNumber(like)
            print("like:{}".format(like))
        except Exception as ex:
            print("Error get like:{}".format(ex))   

        #try to get comment
        try:
            commentElement = postElement.find_element(By.XPATH,'.//*[@data-e2e="comment-count"]')
            comment = commentElement.get_attribute('innerHTML')
            comment = getRealNumber(comment)
            print("comment:{}".format(comment))
        except Exception as ex:
            print("Error get comment:{}".format(ex))

        #try to get share
        try:
            shareElement = postElement.find_element(By.XPATH,'.//*[@data-e2e="share-count"]')
            share = shareElement.get_attribute('innerHTML')
            share = getRealNumber(share)
            print("share:{}".format(share))
        except Exception as ex:
            print("Error get share:{}".format(ex))

        # image = imageElement.get_attribute('src')
        # print("image:{}".format(image))
    except Exception as ex:
        print("Error get post:{}".format(ex))
