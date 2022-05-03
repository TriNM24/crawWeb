import pickle
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from html import unescape
import random
import time
import re
from facebookConstant import facebookConstant as CONT
from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime

from ulties import writeLog
from ulties import writeLogWithName
from ulties import getRealNumber

from telegram.ext import CallbackContext, JobQueue

# seed random number generator
random.seed(time.perf_counter())

mMessage = ''
def sendMessagetoTelegramJob(context: CallbackContext):
    global mMessage
    # context.bot.send_message(chat_id='5051473261', 
    #                          text=mMessage)
    context.bot.send_message(chat_id='-646751586', 
                             text=mMessage)
def sendMessageToTelegram(message, mJobTelegram: JobQueue):
    global mMessage
    mMessage = message
    mJobTelegram.run_once(sendMessagetoTelegramJob,1)

def getRandomTime():
    wait = random.randint(30, 60)
    print("random time:{}".format(wait))
    return wait
def getShortRandomTime():
    wait = random.randint(8, 13)
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
    cleantext = BeautifulSoup(raw_html, "lxml").text
    return cleantext

def loginFace(driver):
    driver.get("https://m.facebook.com/")
    time.sleep(getRandomTime())
    # try to load cookies
    try:
        cookies = pickle.load(open("facebookCookies2.pkl", "rb"))
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        print('Load cookies successfully')
    except Exception as e:
        print("Can not load cookies " + str(e))
    time.sleep(2)
    # reload to login via cookies
    driver.get("https://m.facebook.com/")
    # login if not login yet
    if 'đăng nhập' in driver.title.lower() or 'log in' in driver.title.lower():
        print('Login')
        mail = driver.find_element_by_xpath('//input[@id="m_login_email"]')
        mail.clear()
        mail.send_keys(CONT.facebookUser)

        passInput = driver.find_element_by_xpath('//input[@id="m_login_password"]')
        passInput.clear()
        passInput.send_keys(CONT.facebookPass)

        buttonSubmit = driver.find_element_by_xpath('//button[@name="login"]')
        time.sleep(2)
        print('Submit button ' + buttonSubmit.text)
        buttonSubmit.click()
        WebDriverWait(driver, 10).until(EC.title_contains('Facebook'))

        #try to click ok show in first time
        try:
            okElement = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit" and @value="OK"]')))
            okElement.click()
            time.sleep(getRandomTime())
        except Exception as ex:
            pass

        if os.path.exists("facebookCookies2.pkl"):
            os.remove("facebookCookies2.pkl")
            print('remove file facebookCookies2.pkl')
        pickle.dump(driver.get_cookies(), open("facebookCookies2.pkl", "wb"))
        print('Login final:{}'.format(driver.title))
    else:
        print('Allready login')


class extraData:
    follower = 123456
    extra_info = ["Eve", "Alice", "Bob"]


class FaceBookProfile:    
    name = 'My Laptop'
    avatar = 'Intel Core'
    cover = 'cover'
    extra_data = extraData()

    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getProfileMobile(driver, nameSearch, idFacebookPost, idProfile, mJobTelegram: JobQueue):

    try:
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        logFileName = 'Log/LogFacebookProfile-{}.txt'.format(current_date)

        writeLogWithName(logFileName,'Link face:{}'.format(nameSearch))
        
        try:
            driver.get(nameSearch)
            time.sleep(getRandomTime())
        
            #create data to upload
            dataUpload = FaceBookProfile()
            try:
                nameElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="cover-name-root"] | //body/div[1]/div/div[4]/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div/div')))
                name = nameElement.get_attribute('innerHTML')
                name = cleanhtml(name)                    
                dataUpload.name = name
            except Exception as ex:            
                writeLogWithName(logFileName,"Get name error: {}".format(ex))
                dataUpload.name = ''

            try:            
                imageElement = driver.find_element_by_xpath('//i[@class and @aria-label and @style and @role and contains(@aria-label,"profile picture")]')
                image = imageElement.get_attribute('style')
                start = image.find('url("')
                end = image.find('")')
                image = image[start + 5:end]
                dataUpload.avatar = image            
            except Exception as ex:  
                #try to get avatar for fanpage
                try:            
                    imageElement = driver.find_element_by_xpath('//img[@src and @aria-label and contains(@aria-label,"Ảnh")]')
                    image = imageElement.get_attribute('src')                
                    dataUpload.avatar = image                
                except Exception as ex:              
                    writeLogWithName(logFileName,"Get image error: {}".format(ex))
                    dataUpload.avatar = ''

            try:
                coverImageElement = driver.find_element_by_xpath('//div[@data-sigil="cover-photo"]//i | //a[@data-sigil="cover-photo-link"]/i')
                coverImage = coverImageElement.get_attribute('style')
                start = coverImage.find('url("')
                end = coverImage.find('")')
                coverImage = coverImage[start + 5:end]            
                dataUpload.cover = coverImage
            except Exception as ex:            
                writeLogWithName(logFileName,"Get coverImage error: {}".format(ex))
                dataUpload.cover = 'not have cover photo'

            extra = extraData()
            extra.follower = 0
            infors = []
            try:
                inforElements = driver.find_elements_by_xpath('//div[@id="profile_intro_card"]//div[contains(@data-sigil,"profile-intro-card")]')
                if(len(inforElements) > 0):
                    for inforElement in inforElements:
                        infor = inforElement.get_attribute('innerHTML')
                        infor = cleanhtml(infor).replace('Chi tiết','')
                        print("infor: {}".format(infor))
                        if('theo dõi' in infor):                        
                            extra.follower = getRealNumber(infor)
                        else:
                            infors.append(infor)
                else:
                    try:#try to get infor facebook fanpage
                        elementInformations = driver.find_element_by_xpath('//body/div[1]/div/div[4]/div/div/div/div/div[4]/div/div[2]/div[1]')
                        elementInfos = elementInformations.find_elements_by_xpath("./div[2]/div/div/div/div")
                        for elementInfo1 in elementInfos:
                            dataExtra = cleanhtml(elementInfo1.get_attribute('innerHTML')).strip()
                            if(len(dataExtra) > 0):
                                infors.append(dataExtra)
                    except Exception as ex2:
                        writeLogWithName(logFileName,"get informations error: {}".format(ex2))

            except Exception as ex:
                try:#try to get infor facebook fanpage
                    elementInformations = driver.find_element_by_xpath('//body/div[1]/div/div[4]/div/div/div/div/div[4]/div/div[2]/div[1]')
                    elementInfos = elementInformations.find_elements_by_xpath("./div[2]/div/div/div/div")
                    for elementInfo1 in elementInfos:
                        dataExtra = cleanhtml(elementInfo1.get_attribute('innerHTML')).strip()
                        if(len(dataExtra) > 0):
                            infors.append(dataExtra)
                except Exception as ex2:
                    writeLogWithName(logFileName,"get informations error: {}".format(ex2))

            #try to get flower for fanpage
            try:
                likeElement = driver.find_element_by_xpath('//body/div[1]/div/div[4]/div/div[1]/div/div/div[1]/div/div[4]/div')
                likeNumber = likeElement.get_attribute('innerHTML')
                likeNumber = cleanhtml(likeNumber)
                likeNumberInt = re.sub(r'[^0-9]',r'',likeNumber)
                if(len(likeNumberInt) > 0):
                    # likeNumberInt = re.sub(r'[^0-9k.,]',r'',likeNumber)                   
                    extra.follower = getRealNumber(likeNumber)
                else:
                    likeElement = driver.find_element_by_xpath('//body/div[1]/div/div[4]/div/div[1]/div/div/div[1]/div/div[5]/div')
                    likeNumber = likeElement.get_attribute('innerHTML')
                    likeNumber = cleanhtml(likeNumber)
                    likeNumberInt = re.sub(r'[^0-9]',r'',likeNumber)
                    if(len(likeNumberInt) > 0):
                        # likeNumberInt = re.sub(r'[^0-9k.,]',r'',likeNumber)                   
                        extra.follower = getRealNumber(likeNumber)
            except Exception as ex:            
                writeLogWithName(logFileName,"Get like fanpage error: {}".format(ex))

            if(len(infors) == 0):
                infors.append('Do not have info')
                
            extra.extra_info = infors
            dataUpload.extra_data = extra
            uploadFacebookInfo(dataUpload, idProfile, logFileName, mJobTelegram, nameSearch)

            # try to get 30 posts
            getPostsFromProfile(driver, logFileName, mJobTelegram, nameSearch, idFacebookPost, idProfile)
        except Exception as ex:        
            writeLogWithName(logFileName,'get data fail: {}'.format(ex))
    except Exception as ex:
        writeLogWithName(logFileName,'Error catch all: {}'.format(ex))
        sendMessageToTelegram("Error catch all: {}".format(ex), mJobTelegram)

def uploadFacebookInfo(data:FaceBookProfile, idFacebook, logFileName, mJobTelegram: JobQueue, link):
    api_url_post = "http://42.119.111.90:8080/crawl/influencer/{}/facebook".format(idFacebook)
    headers =  {"Content-Type":"application/json"}
    responsePost = requests.post(api_url_post, json=data.toJson(), headers=headers)    
    # writeLogWithName(logFileName,'Json response post:{}'.format(responsePost.json()))
    writeLogWithName(logFileName,'Status response:{}'.format(responsePost.status_code))
    if(responsePost.status_code != 200):
        sendMessageToTelegram("Error upload profile facebook {}".format(link), mJobTelegram)

class FaceBookPost:    
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
    tags = []
    
    def toJson(self):
        jsonStr = json.dumps(self, default=lambda o: o.__dict__)
        return json.loads(jsonStr)

def getPostsFromProfile(driver, logFileName, mJobTelegram: JobQueue, link, idFacebookPost, idProfile):
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')

    scrollTime = 0
    keepScroll = 1
    while keepScroll > 0:
        scrollTime = scrollTime + 1
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")        
        # Wait to load page
        time.sleep(getShortRandomTime())
        inforElements = driver.find_elements_by_xpath('//article')
        if(len(inforElements) >= 60):
            keepScroll = 0
        elif(scrollTime > 10):
            keepScroll = 0            
            #send message to telegram
            sendMessageToTelegram("{} Can not srcoll after 10 time, size:{} -> please check:{}".format(current_date,len(inforElements),link), mJobTelegram)
            writeLogWithName(logFileName,'Can not srcoll after 10 time')
    
    try:
        inforElements = driver.find_elements_by_xpath('//article')

        count = 0
        for inforElement in inforElements:
            count = count + 1
            if(count > 60):
                break    
            try:
                idInfor = inforElement.get_attribute('data-store')
                jsonInfor = json.loads(idInfor)
                idData = jsonInfor['share_id']
            except Exception as ex:
                writeLogWithName(logFileName,'Error get id:{}'.format(ex))
                continue
            
            dataPost = FaceBookPost()
            dataPost.object_id = idData
            dataPost.influencer_id = idFacebookPost
            dataPost.influencer_platform_id = idProfile
            
            try:
                timeElement = inforElement.find_element_by_xpath('.//header/div/div[2]/div/div/div/div[1]/div')
                timeInfo = timeElement.get_attribute('innerHTML')
                timeInfo = cleanhtml(timeInfo)
                dataPost.post_time = timeInfo
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get time:{}'.format(ex))
            
            try:
                linkElement = inforElement.find_element_by_xpath('.//header/div/div[2]/div/div/div/div[1]/div/a')
                link = linkElement.get_attribute('href')                                
                dataPost.link = link
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get link:{}'.format(ex))

            try:
                contentElement = inforElement.find_element_by_xpath('./div/div[1]')
                content = contentElement.get_attribute('innerHTML')
                content = cleanhtml(content)
                dataPost.content = content
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get content:{}'.format(ex))

            dataHasgTag = []
            try:
                hashTagElements = inforElement.find_elements_by_xpath('.//a[contains(@href,"hashtag")]')
                for hashTagElement in hashTagElements:
                    hashtag = hashTagElement.get_attribute('innerHTML')
                    hashtag = cleanhtml(hashtag)
                    dataHasgTag.append(hashtag)                    
                dataPost.tags = dataHasgTag
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get hashtag:{}'.format(ex))    
    
            try:
                LikeElement = inforElement.find_element_by_xpath('./footer/div/div[1]/a/div/div[1]')
                like = LikeElement.get_attribute('innerHTML')
                like = cleanhtml(like)
                dataPost.like = getRealNumber(like)
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get like:{}'.format(ex))
                dataPost.like = '0'

            try:
                commentElement = inforElement.find_element_by_xpath('./footer/div/div[1]/a/div/div[2]/span[1]')
                comment = commentElement.get_attribute('innerHTML')
                comment = cleanhtml(comment)
                dataPost.comment = getRealNumber(comment)
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get comment:{}'.format(ex))
                dataPost.comment = '0'

            try:
                shareElement = inforElement.find_element_by_xpath('./footer/div/div[1]/a/div/div[2]/span[2]')
                share = shareElement.get_attribute('innerHTML')
                share = cleanhtml(share)                
                dataPost.share = getRealNumber(share)
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get share:{}'.format(ex))
                dataPost.share = '0'

            dataVideo = []
            dataImage = []
            # try to get images
            try:                
                imagesElement = inforElement.find_elements_by_xpath('./div/div[2]//a//i')
                for imageElement in imagesElement:
                    image = imageElement.get_attribute('style')
                    start = image.find('url("')
                    end = image.find('")')
                    image = image[start + 5:end]                    
                    dataImage.append(image)
                dataPost.content_type = "photo"                
            except Exception as ex:                
                writeLogWithName(logFileName,'Error get images:{}'.format(ex))
                #try to get video
                try:                    
                    videoElement = inforElement.find_element_by_xpath('./div/div[2]/div[1]/div/div[@data-store] | .//section/div/div[@data-store]')
                    videoData = videoElement.get_attribute('data-store')
                    jsonVideo = json.loads(videoData)
                    videoLink = jsonVideo['src']
                    dataVideo.append(videoLink)
                    dataPost.content_type = "video"
                except Exception as ex:                    
                    writeLogWithName(logFileName,'Error get videoLink:{}'.format(ex))
                    # try to get link share
                    try:
                        shareElement = inforElement.find_element_by_xpath('./div/div[2]/section/a')
                        shareLink = shareElement.get_attribute('href')
                        dataPost.content = '{}\n{}'.format(dataPost.content,shareLink)
                        dataPost.content_type = "share"
                    except Exception as ex:                        
                        writeLogWithName(logFileName,'Error get shareLink:{}'.format(ex))

            dataPost.image = dataImage
            dataPost.video = dataVideo
            dataPost.platform_code = 'facebook'
            uploadFacebookPost(dataPost,logFileName)
        
    except Exception as ex:        
        writeLogWithName(logFileName,'Error Total get post:{}'.format(ex))

def uploadFacebookPost(data:FaceBookPost, logFileName):
    api_url_post = "http://42.119.111.90:8080/crawl/post"
    headers =  {"Content-Type":"application/json"}
    responsePost = requests.post(api_url_post, json=data.toJson(), headers=headers)    
    # writeLogWithName(logFileName,'Json response post:{}'.format(responsePost.json()))
    writeLogWithName(logFileName,'Status response:{}'.format(responsePost.status_code))


def getPosts(driver, nameSearch):
    writeLog('get post: {}'.format(nameSearch))
    driver.get(nameSearch)
    time.sleep(getRandomTime())
    scrollTime = 0
    while scrollTime >= 0:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('scroll time {}'.format(scrollTime))
        # Wait to load page
        time.sleep(getShortRandomTime())
        inforElements = driver.find_elements_by_xpath('//article')
        print('Post number:{}'.format(len(inforElements)))
        if(len(inforElements) >= 30):
            scrollTime = scrollTime - 1
    
    try:
        inforElements = driver.find_elements_by_xpath('//article')
        for inforElement in inforElements:

            idInfor = inforElement.get_attribute('data-store')
            jsonInfor = json.loads(idInfor)
            idData = jsonInfor['share_id']
            print("\nId post:{}".format(idData))

            try:
                timeElement = inforElement.find_element_by_xpath('.//header/div/div[2]/div/div/div/div[1]/div')
                timeInfo = timeElement.get_attribute('innerHTML')
                timeInfo = cleanhtml(timeInfo)
                print("Time:{}".format(timeInfo))
            except Exception as ex:
                print('Error get time:{}'.format(ex))
            
            try:
                linkElement = inforElement.find_element_by_xpath('.//header/div/div[2]/div/div/div/div[1]/div/a')
                link = linkElement.get_attribute('href')                
                print("Link:{}".format(link))
            except Exception as ex:
                print('Error get time:{}'.format(ex))

            try:
                contentElement = inforElement.find_element_by_xpath('./div/div[1]')
                content = contentElement.get_attribute('innerHTML')
                content = cleanhtml(content)
                print("Content:{}".format(content))
            except Exception as ex:
                print('Error get content:{}'.format(ex))

            try:
                LikeElement = inforElement.find_element_by_xpath('./footer/div/div[1]/a/div/div[1]')
                like = LikeElement.get_attribute('innerHTML')
                like = cleanhtml(like)
                print("Like:{}".format(like))
            except Exception as ex:
                print('Error get like:{}'.format(ex))  

            try:
                commentElement = inforElement.find_element_by_xpath('./footer/div/div[1]/a/div/div[2]')
                comment = commentElement.get_attribute('innerHTML')
                comment = cleanhtml(comment)
                print("Comment:{}".format(comment))
            except Exception as ex:
                print('Error get comment:{}'.format(ex))   

            # try to get images
            try:
                imagesElement = inforElement.find_elements_by_xpath('./div/div[2]//a//i')
                for imageElement in imagesElement:
                    image = imageElement.get_attribute('style')
                    start = image.find('url("')
                    end = image.find('")')
                    image = image[start + 5:end]
                    print("Image: {}".format(image))        
            except Exception as ex:
                print('Error get images:{}'.format(ex))

            #try to get video
            try:
                videoElement = inforElement.find_element_by_xpath('./div/div[2]/div[1]/div/div[@data-store] | .//section/div/div[@data-store]')
                videoData = videoElement.get_attribute('data-store')
                jsonVideo = json.loads(videoData)
                videoLink = jsonVideo['src']            
                print("videoLink:{}".format(videoLink))
            except Exception as ex:
                print('Error get videoLink:{}'.format(ex))

            # try to get link share
            try:
                shareElement = inforElement.find_element_by_xpath('./div/div[2]/section/a')
                shareLink = shareElement.get_attribute('href')                       
                print("shareLink:{}".format(shareLink))
            except Exception as ex:
                print('Error get shareLink:{}'.format(ex))
        
    except Exception as ex:
        print('Error:{}'.format(ex))
