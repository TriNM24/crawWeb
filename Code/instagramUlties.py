from email import utils
import pickle
from tkinter import image_names
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from html import unescape
import random
import time
import re
from instagramConstant import IntagramConstant as CONT
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from ulties import writeLogWithName
import json
import requests
from datetime import datetime
from ulties import getRealNumber
from seleniumwire.utils import decode

from telegram.ext import CallbackContext, JobQueue

# seed random number generator
random.seed(time.perf_counter())

mMessage = ''
def sendMessagetoTelegramJob(context: CallbackContext):
    global mMessage
    context.bot.send_message(chat_id='-656309040', 
                             text=mMessage)
def sendMessageToTelegram(message, mJobTelegram: JobQueue):
    global mMessage
    mMessage = message
    mJobTelegram.run_once(sendMessagetoTelegramJob,1)


def getRandomTime():
    wait = random.randint(60, 120)
    print("random time:{}".format(wait))
    return wait

def getRandomTimeShort():
    wait = random.randint(10, 20)
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

def loginIntagram(driver):
    # init domain
    driver.get("https://www.instagram.com/accounts/login/")
    try:
        cookies = pickle.load(open(CONT.cookies_file, "rb"))
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        print('Load cookies successfully')
    except Exception as e:
        print("Can not load cookies " + str(e))
    # reload to login via cookies
    driver.get("https://www.instagram.com/accounts/login/")
    if 'login' in driver.title.lower():
        try:
            mail = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, CONT.xpathMail)))
            mail.clear()
            mail.send_keys(CONT.userName)
            passElement = driver.find_element_by_xpath(CONT.xpathPass)
            passElement.clear()
            passElement.send_keys(CONT.passWord)
            # try to click button Accept all cookies
            try:
                btnAcceptAll = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.xpathAcceptAll)))
                print('click button Accept All cookies')
                btnAcceptAll.click()
            except Exception as ex:
                print("Do not have button Accept all cookies")
            buttonLogin = driver.find_element_by_xpath(CONT.xpathButtonLogin)
            print('Submit button ' + buttonLogin.text)
            buttonLogin.click()
            try:
                action = ActionChains(driver)
                buttonNotNow = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, CONT.notNowButtonSaveInfo)))
                print("click butotn not now in save information")
                time.sleep(2)
                action.move_to_element(buttonNotNow).click(buttonNotNow).perform()
                time.sleep(5)
                # save cookies
                if os.path.exists(CONT.cookies_file):
                    os.remove(CONT.cookies_file)
                    print('remove file {}'.format(CONT.cookies_file))
                pickle.dump(driver.get_cookies(), open(
                    CONT.cookies_file, "wb"))
                print("Login and save cookies success")
            except Exception as ex:
                print("Button not now:{}".format(ex))

        except NoSuchElementException as noelementex:
            print('Can not find button login')
    else:
        print('Allready login')


class extraData:
    follower = 123456
    post = 0
    follow = 0
    extra_info = ["Eve", "Alice", "Bob"]


class InstagramProfile:    
    name = 'My Laptop'
    avatar = 'Intel Core'    
    extra_data = extraData()

    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getInfoIntagram(driver, link, idInstagramPost, idProfile, mJobTelegram: JobQueue):

    try:
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        logFileName = 'Log/LogInstagramProfile-{}.txt'.format(current_date)
        writeLogWithName(logFileName,'Link: {}'.format(link))
        try:            
            driver.get(link)            
        except Exception as ex:
            time.sleep(3)
            driver.get(link)
        
        time.sleep(getRandomTime())

        try:
            dataPost = InstagramProfile()
            try:
                elementImage = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, CONT.xpathImage)))
                image = elementImage.get_attribute('src')
                dataPost.avatar = image
            except Exception as ex:
                dataPost.avatar = ''
                writeLogWithName(logFileName,'Error get image: {}'.format(ex))

            try:
                elementName = driver.find_element_by_xpath(CONT.xpathName)
                name = elementName.get_attribute('innerHTML')
                dataPost.name = name
            except Exception as ex:
                dataPost.name = ''
                writeLogWithName(logFileName,'Error get name: {}'.format(ex))

            extra = extraData()
            extra.follow = 0
            extra.follower = 0
            extra.post = 0
            infors = []
            try:
                elementInformations = driver.find_element_by_xpath(CONT.xpathInfo)
                elementInfos = elementInformations.find_elements_by_xpath("./li")        
                for elementInfo1 in elementInfos:
                    dataExtra = cleanhtml(elementInfo1.get_attribute('innerHTML'))
                    if('posts' in dataExtra):
                        # postInt = re.sub(r'[^0-9k.,]',r'',dataExtra)
                        extra.post = getRealNumber(dataExtra)
                    if('followers' in dataExtra):
                        # followerInt = re.sub(r'[^0-9k.,]',r'',dataExtra)
                        extra.follower = getRealNumber(dataExtra)
                    if('following' in dataExtra):
                        # followingInt = re.sub(r'[^0-9k.,]',r'',dataExtra)
                        extra.follow = getRealNumber(dataExtra)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get infor: {}'.format(ex))

            try:
                elementExtendInfo = driver.find_element_by_xpath(CONT.xpathExtendInfo)
                extraInfo = cleanhtml(elementExtendInfo.get_attribute('innerHTML'))
                infors.append(extraInfo)
                extra.extra_info = infors
            except Exception as ex:
                writeLogWithName(logFileName,'Error get extend infor: {}'.format(ex))            

            dataPost.extra_data = extra            
            uploadInstagramInfo(dataPost, idProfile, logFileName, mJobTelegram, link)

            #get posts
            getInstagramPost(driver,idInstagramPost, idProfile, logFileName, mJobTelegram)

        except Exception as ex:
            writeLogWithName(logFileName,'Error get infor: {}'.format(ex))
    except Exception as ex:
        writeLogWithName(logFileName,'Error catch all: {}'.format(ex))
        sendMessageToTelegram("Error catch all: {}".format(ex), mJobTelegram)

def uploadInstagramInfo(data:InstagramProfile, idInstagram, logFileName, mJobTelegram: JobQueue, link):
    api_url_post = "http://42.119.111.90:8080/crawl/influencer/{}/instagram".format(idInstagram)
    headers =  {"Content-Type":"application/json"}
    responsePost = requests.post(api_url_post, json=data.toJson(), headers=headers)    
    writeLogWithName(logFileName,'Json response post:{}'.format(responsePost.json()))
    writeLogWithName(logFileName,'Status response:{}'.format(responsePost.status_code))
    if(responsePost.status_code != 200):
        sendMessageToTelegram("Error post profile instagram {}".format(link), mJobTelegram)

class DataPost:
    object_id = ''
    post_time = ''
    platform_code = ''
    influencer_id = ''
    influencer_platform_id = ''
    link = ''
    content = ''
    image = []
    video = []
    like = ''
    share = ''
    comment = ''
    tags = []
    
    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getInstagramPost(driver, idInstagramPost, idProfile, logFileName, mJobTelegram: JobQueue):
    
    try:
        isExist = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,"//body/div[1]//section/main/div/div[3]/article/div[1]/div/div/div")))
        elementPosts = driver.find_elements(By.XPATH,"//body/div[1]//section/main/div/div[3]/article/div[1]/div/div/div")

        count = 0
        for elementPost in elementPosts:

            count = count + 1
            if(count > 10):
                break

            dataPost = DataPost()
            dataPost.platform_code = 'instagram'
            dataPost.influencer_id = idInstagramPost
            dataPost.influencer_platform_id = idProfile
            dataPost.content = 'image'
            dataPost.video = []

            imageData = []

            scroll_shim(driver,elementPost)
            time.sleep(2)
            action = ActionChains(driver)     
            action.move_to_element(elementPost).perform()
            time.sleep(2)            
            try:
                # get like        
                likeElement = elementPost.find_element(By.XPATH,"/a/div[3]/ul/li[1]/div")
                like = likeElement.get_attribute('innerHTML')            
                dataPost.like = getRealNumber(like)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get like:{}'.format(ex))
                dataPost.like = 0
                #send message to check xpath get like
                #sendMessageToTelegram("Error get like instagram: {}".format(ex), mJobTelegram)

            try:
                # get comment
                commentElement = elementPost.find_element(By.XPATH,"./a/div[3]/ul/li[2]/div")
                comment = commentElement.get_attribute('innerHTML')            
                dataPost.comment = getRealNumber(comment)
            except Exception as ex:
                writeLogWithName(logFileName,'Error get comment:{}'.format(ex))
                dataPost.comment = 0

            # get image
            imageElement = elementPost.find_element(By.XPATH,".//img")
            image = unescape(imageElement.get_attribute("src"))            
            imageData.append(image)
            dataPost.image = imageData
            # get link
            linkElement = elementPost.find_element(By.XPATH,"./a")
            link = linkElement.get_attribute('href')            
            dataPost.link = link
            idSplit = link.split('/')            
            dataPost.object_id = idSplit[len(idSplit)-2]

            try:
                action = ActionChains(driver)
                action.move_to_element(elementPost).click(elementPost).perform()

                # get time                
                timeElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article/div/div[2]/div/div/div[2]/div[2]/a/time | //article/div/div[2]/div/div/div[2]/div[2]/div/a/div/time")))                
                timeData = timeElement.get_attribute('innerHTML')
                dataPost.post_time = timeData

                #get hashtag
                dataHasgTag = []
                try:
                    hashTagElements = driver.find_elements_by_xpath('//span/a[contains(@href,"tags")]')
                    for hashTagElement in hashTagElements:
                        hashtag = hashTagElement.get_attribute('innerHTML')
                        hashtag = cleanhtml(hashtag)
                        dataHasgTag.append(hashtag)                        
                    dataPost.tags = dataHasgTag
                except Exception as ex:                
                    writeLogWithName(logFileName,'Error get hashtag:{}'.format(ex))

                time.sleep(getRandomTimeShort())
                # close
                closeElement = driver.find_element(By.XPATH,'//body/div[6]/div[1]/button | //button//*[@aria-label="Đóng"]')
                action = ActionChains(driver)
                action.move_to_element(closeElement).click(closeElement).perform()
            except Exception as ex:                
                writeLogWithName(logFileName,"Error get time: {}".format(ex))
            
            # post data
            uploadDataPost(dataPost,logFileName)

    except Exception as ex:        
        writeLogWithName(logFileName,"UnHandle except: {}".format(ex))

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
    # time.sleep(getRandomTime())
    time.sleep(5)

    try:
        imageElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@style,"padding-bottom")]/img')))
        image = imageElement.get_attribute('src')
        print("image:{}".format(image))
    except Exception as ex:
        print("Error get image:{}".format(ex))

    try:
        likeElement = driver.find_element(By.XPATH,'//a[contains(@href,"liked")]')
        like = likeElement.get_attribute('innerHTML')
        like = cleanhtml(like)
        like = getRealNumber(like)
        print("Like:{}".format(like))
    except Exception as ex:
        print("Error get like:{}".format(ex))

    # try to get comment number
    try:
        action = ActionChains(driver)
        buttonLoadmore  = driver.find_element_by_xpath("//body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button")
        driver.execute_script("arguments[0].scrollIntoView();", buttonLoadmore)
        time.sleep(5)
        scroll_shim(driver,buttonLoadmore)
        time.sleep(2)
        action.move_to_element(buttonLoadmore).perform()
        time.sleep(5)
        buttonLoadmore.click()
        time.sleep(5)
        for request in driver.requests:
            if request.response:
                if("/comments/" in request.url):
                    body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                    body2 = body.decode('utf-8')                    
                    if('"comment_count":' in body2):
                        comment = body2.split('"comment_count":',1)[1].split(',')[0]
                        print("comment: {}".format(comment))
                        break


    except Exception as ex:
        print("Error get comment count:{}".format(ex))


    
    
