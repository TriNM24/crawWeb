import argparse
from os import replace
import sys
from time import sleep, time
import ulties
from seleniumwire import webdriver
import multiprocessing as mp
from selenium.webdriver.remote.webdriver import WebDriver
import facebookUlties
import instagramUlties
import youtubeUlties
import tiktokUlties
from datetime import datetime
import requests
import json
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext, JobQueue

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

mDriver: WebDriver
mJobTelegram: JobQueue

mMessage = ''
def sendMessagetoTelegramJob(context: CallbackContext):
    global mMessage
    context.bot.send_message(chat_id='5051473261', 
                             text=mMessage)
def sendMessageToTelegram(message, mJobTelegram: JobQueue):
    global mMessage
    mMessage = message
    mJobTelegram.run_once(sendMessagetoTelegramJob,1)

def main(args):
    parser = argparse.ArgumentParser(description="Do something.")
    parser.add_argument("-f", "--function", type=float, default=4, required=False)
    args = parser.parse_args(args)

    print("input:{}".format(args.function))
    callFunction(args.function)

    quit()

def callFunction(i):
    switcher = {
        1: facebookInfor,
        2: facebookPosts,
        3: instagramInfor,
        4: youtubeInfor,
        5: tiktokInfor,
        6: getInstagramPost,
        7: manualLoginTiktok,
        8: testLog,
        9: callAPI
    }
    func = switcher.get(i)
    return func()

#get next page to get data
def getPageToGet(savedFile):
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    nextPage = 1
    try:
        with open(savedFile, 'r', encoding='UTF-8') as file:
            line = file.readline().rstrip()            
            nextPage = line.split(',')[0]
    except Exception as ex:
        pass
    if(nextPage == '-1'):
        #update next page
        with open(savedFile, 'w') as filetowrite:
            filetowrite.write('{},{}'.format(str(1), current_date))
        print('Stop run because nextpage is -1')
        quit() #stop run
    return nextPage

def saveNextPage(savedFile, currentPage, totalPage):
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    # write nextpage
    file = savedFile
    with open(file, 'w') as filetowrite:
        if(currentPage+1 > totalPage):
            # write -1 to not run next time
            filetowrite.write('-1,{}'.format(current_date))
        else:
            filetowrite.write('{},{}'.format(str(currentPage+1), current_date))

def facebookInfor():

    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    # get next page to get data
    nextPage = getPageToGet('nextPageFacebook.txt')
    logFileName = 'Log/LogFacebookProfile-{}.txt'.format(current_date)
    ulties.writeLogWithName(logFileName,'________________Get page________________: {}'.format(nextPage))

    api_url_get = "http://42.119.111.90:8080/crawl/influencer?page={}&platform[]=facebook".format(nextPage)
    responseGet = requests.get(api_url_get)
    jsonData = responseGet.json()
    currentPage = jsonData['meta']['pagination']['current_page']
    totalPage = jsonData['meta']['pagination']['total_pages']
    ulties.writeLogWithName(logFileName,'TotalPage : {}'.format(totalPage))
    # write nextpage
    saveNextPage('nextPageFacebook.txt', currentPage, totalPage)   

    global mDriver
    mDriver = ulties.build_driver2()
    # facebookUlties.loginFace(mDriver)

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5075461862:AAGO-zhcRGVbkh0mumXuTXHwt1jDWvopgAo", use_context=True)    
    # Start the Bot
    updater.start_polling()
    mJobTelegram = updater.job_queue

    #start to get all data
    for item in jsonData['data']:
        ulties.writeLogWithName(logFileName,'Facebook name: {}'.format(item['name']))
        if(item['facebook'] is None):
            print('link emply')
        else:
            for link in item['facebook']:
                linkGet = link['link'].replace('www', 'm')
                facebookUlties.getProfileMobile(mDriver, linkGet, item['id'], link['id'], mJobTelegram)
    #stop bot
    updater.stop()
    mDriver.close()
    mDriver.quit()


def facebookPosts():
    print("Get facebook posts")
    global mDriver
    mDriver = ulties.build_driver2()
    # facebookUlties.loginFace(mDriver)
    # facebookUlties.getPosts(mDriver, "https://m.facebook.com/bacsiduyen")

    updater = Updater("5075461862:AAGO-zhcRGVbkh0mumXuTXHwt1jDWvopgAo", use_context=True)    
    # Start the Bot
    updater.start_polling()
    mJobTelegram = updater.job_queue
    facebookUlties.getProfileMobile(mDriver, "https://m.facebook.com/Hailey-Thu%E1%BB%B3-L%C3%AA-107777034264886/",37,mJobTelegram)
    
    # instagramUlties.getInfoIntagram(mDriver, "https://www.instagram.com/bchnathu/",31)
    # youtubeUlties.getInfoYoutube(mDriver, 'https://www.youtube.com/channel/UChb5rg2sO4RKPTvJl0bfPPA/featured',6)
    # youtubeUlties.getPosts(mDriver, 'https://www.youtube.com/channel/UChb5rg2sO4RKPTvJl0bfPPA/featured')


def instagramInfor():
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    # get next page to get data
    nextPage = getPageToGet('nextPageInstagram.txt')
    logFileName = 'Log/LogInstagramProfile-{}.txt'.format(current_date)
    ulties.writeLogWithName(logFileName,'________________Get page________________: {}'.format(nextPage))

    api_url_get = "http://42.119.111.90:8080/crawl/influencer?page={}&platform[]=instagram".format(nextPage)
    responseGet = requests.get(api_url_get)
    jsonData = responseGet.json()
    currentPage = jsonData['meta']['pagination']['current_page']
    totalPage = jsonData['meta']['pagination']['total_pages']
    ulties.writeLogWithName(logFileName,'TotalPage : {}'.format(totalPage))
    # write nextpage
    saveNextPage('nextPageInstagram.txt', currentPage, totalPage)

    global mDriver
    mDriver = ulties.build_driver2()
    # instagramUlties.loginIntagram(mDriver)

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5008862971:AAGZT80XRt3grWAT3nBvaN8oQ28mNkQCSJQ", use_context=True)    
    # Start the Bot
    updater.start_polling()
    mJobTelegram = updater.job_queue

    #start to get all data
    for item in jsonData['data']:
        ulties.writeLogWithName(logFileName,'Instagram name: {}'.format(item['name']))
        if(item['instagram'] is None):
            print('link emply')
        else:
            for link in item['instagram']:
                linkGet = link['link']                
                instagramUlties.getInfoIntagram(mDriver, linkGet, item['id'], link['id'], mJobTelegram)
    #stop bot
    updater.stop()
    mDriver.close()
    mDriver.quit()

def youtubeInfor():

    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    # get next page to get data
    nextPage = getPageToGet('nextPageYoutube.txt')
    logFileName = 'Log/LogInsYoutubeProfile-{}.txt'.format(current_date)
    ulties.writeLogWithName(logFileName,'________________Get page________________: {}'.format(nextPage))

    api_url_get = "http://42.119.111.90:8080/crawl/influencer?page={}&platform[]=youtube".format(nextPage)
    responseGet = requests.get(api_url_get)
    jsonData = responseGet.json()
    currentPage = jsonData['meta']['pagination']['current_page']
    totalPage = jsonData['meta']['pagination']['total_pages']
    ulties.writeLogWithName(logFileName,'TotalPage : {}'.format(totalPage))
    # write nextpage
    saveNextPage('nextPageYoutube.txt', currentPage, totalPage)

    global mDriver
    mDriver = ulties.build_driver2()

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5018141494:AAHuvI7BgVJ_RzGXGVzLuTB2OUe4M80icec", use_context=True)    
    # Start the Bot
    updater.start_polling()
    mJobTelegram = updater.job_queue

    #start to get all data
    for item in jsonData['data']:
        ulties.writeLogWithName(logFileName,'Yotube name: {}'.format(item['name']))
        if(item['youtube'] is None):
            print('link emply')
        else:
            for link in item['youtube']:
                linkGet = link['link']
                youtubeUlties.getInfoYoutube(mDriver, linkGet, item['id'], link['id'], mJobTelegram)

    #stop bot
    updater.stop()
    mDriver.close()
    mDriver.quit()

def tiktokInfor():
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    # get next page to get data
    nextPage = getPageToGet('nextPageTiktok.txt')
    logFileName = 'Log/LogTiktokProfile-{}.txt'.format(current_date)
    ulties.writeLogWithName(logFileName,'________________Get page________________: {}'.format(nextPage))

    api_url_get = "http://42.119.111.90:8080/crawl/influencer?page={}&platform[]=tiktok".format(nextPage)
    responseGet = requests.get(api_url_get)
    jsonData = responseGet.json()
    currentPage = jsonData['meta']['pagination']['current_page']
    totalPage = jsonData['meta']['pagination']['total_pages']
    ulties.writeLogWithName(logFileName,'TotalPage : {}'.format(totalPage))
    # write nextpage
    saveNextPage('nextPageTiktok.txt', currentPage, totalPage)

    global mDriver
    mDriver = ulties.build_driver2()

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5037109268:AAFk8iEvCgHUA3VJSGQ8oCxJsaDssQtwl-E", use_context=True)    
    # Start the Bot
    updater.start_polling()
    mJobTelegram = updater.job_queue

    #start to get all data
    for item in jsonData['data']:
        ulties.writeLogWithName(logFileName,'Tiktok name: {}'.format(item['name']))
        if(item['tiktok'] is None):
            print('link emply')
        else:
            for link in item['tiktok']:
                linkGet = link['link']
                tiktokUlties.getInfoTiktok(mDriver, linkGet, item['id'], link['id'], mJobTelegram)

    #stop bot
    updater.stop()
    mDriver.close()
    mDriver.quit()

def getInstagramPost():
    global mDriver
    mDriver = ulties.build_driver2()
    instagramUlties.getPostDetail(mDriver,'https://www.instagram.com/p/CZ9IxIgJ8as/')

    mDriver.close()
    mDriver.quit()


def manualLoginTiktok():
    print("Manual login tiktok")
    global mDriver
    mDriver = ulties.build_driver2()
    tiktokUlties.manualLoginAndSaveCokies(mDriver)

def testLog():
    testString = "Vũ Trần Kim Nhã và 2.2M người khác"
    # Vũ Trần Kim Nhã và 22K người khác
    # Vũ Trần Kim Nhã và 2.2k người khác
    # Vũ Trần Kim Nhã và 2.2M người khác
    # Vũ Trần Kim Nhã và 123 người khác

    number = ulties.getRealNumber(testString)
    print(number)    

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

import re
def callAPI():
    test = '1.4k nguoi khac'
    test2 = '207k followers'
    nestr = re.sub(r'[^0-9k.,]',r'',test)
    nestr2 = re.sub(r'[^0-9k.,]',r'',test2)
    print(nestr.strip())
    print(nestr2.strip())
    ab = ulties.getRealNumber(test)


if __name__ == '__main__':
    main(sys.argv[1:])

