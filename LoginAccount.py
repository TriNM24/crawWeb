from warnings import catch_warnings
from MyConstants import Facebook
from MyConstants import Intagram
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from html import unescape
import Constant_intagram as constant
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import re

def scroll_shim(passed_in_driver, object):  # scroll to element
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def loginIntagram(driver):
    constant = Intagram()
    print('Login')
    try:
        mail = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, constant.xpathMail)))
        mail.clear()
        mail.send_keys(constant.userName)
        passElement = driver.find_element_by_xpath(constant.xpathPass)
        passElement.clear()
        passElement.send_keys(constant.passWord)
        # try to click button Accept all cookies
        try:
            btnAcceptAll = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, constant.xpathAcceptAll)))
            print('click button Accept All cookies')
            btnAcceptAll.click()
        except Exception as ex:
            print("Do not have button Accept all cookies")
        buttonLogin = driver.find_element_by_xpath(constant.xpathButtonLogin)
        print('Submit button ' + buttonLogin.text)
        buttonLogin.click()
        try:
            action = ActionChains(driver)
            buttonNotNow = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, constant.notNowButtonSaveInfo)))
            print("click butotn not now in save information")
            time.sleep(2)
            action.move_to_element(buttonNotNow).click(buttonNotNow).perform()
            time.sleep(5)
            # save cookies
            if os.path.exists(constant.cookies_file):
                os.remove(constant.cookies_file)
                print('remove file {}'.format(constant.cookies_file))
            pickle.dump(driver.get_cookies(), open(
                constant.cookies_file, "wb"))
            print("Login and save cookies success")
        except Exception as ex:
            print("Button not now:{}".format(ex))

    except NoSuchElementException as noelementex:
        print('Can not find button login')


def loginFace(driver):
    print(driver.title)
    CONT = Facebook()
    mail = driver.find_element_by_xpath(CONT.xpathEmail)
    mail.clear()
    mail.send_keys(CONT.facebookUser)

    passInput = driver.find_element_by_xpath(CONT.xpathPass)
    passInput.clear()
    passInput.send_keys(CONT.facebookPass)

    buttonSubmit = driver.find_element_by_xpath(CONT.xpathSubmit)
    print('Submit button ' + buttonSubmit.text)
    buttonSubmit.click()
    WebDriverWait(driver, 10).until(EC.title_is('Facebook'))
    if os.path.exists("cookies.pkl"):
        os.remove("cookies.pkl")
        print('remove file cookies.pkl')
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def getFacePost(driver, nameFace):
    print('get data' + driver.title)
    CONT = Facebook()
    driver.get("https://www.facebook.com/" + nameFace)

    SCROLL_PAUSE_TIME = 2
    scrollTime = 1
    while scrollTime >= 0:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('scroll time {}'.format(scrollTime))
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        scrollTime = scrollTime - 1

    # get all data
    try:
        wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div")))
        elementPosts = driver.find_elements_by_xpath(
            "//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[3]/div")
        for elementPost in elementPosts:
            #get link post
            try:
                time.sleep(3)
                dotElement = elementPost.find_element_by_xpath(".//div[2]/div/div[2]/div/div[3]/div")
                scroll_shim(driver,dotElement)
                dotElement.click()
                time.sleep(2)

                menuEmbeddeds = driver.find_elements_by_xpath("//body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div")
                for menuEmbeddedElemnt in menuEmbeddeds:
                    menuEmbedded = menuEmbeddedElemnt.find_element_by_xpath("./div[2]/div/div/span")
                    if('Nhúng' in menuEmbedded.get_attribute('innerHTML')):
                        menuEmbedded.click()
                        time.sleep(3)
                        postLinkElement = driver.find_element_by_xpath("//body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[1]/label/input")
                        postLink = unescape(postLinkElement.get_attribute('value'))
                        print("postLink: {}".format(postLink))
                        closeElement = driver.find_element_by_xpath("//body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div")
                        closeElement.click()
            except Exception as ex:
                pass

            # get time post
            timeElement = elementPost.find_element_by_xpath(
                ".//div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a/span/span/b")
            timePost = timeElement.find_element_by_xpath(".//b[not(@style)]").get_attribute('innerHTML')
            print("timePost: {}".format(timePost))
            #get like
            likeElement = elementPost.find_element_by_xpath(
                ".//div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span")
            likeNumber = likeElement.get_attribute('innerHTML')
            print("likeNumber: {}".format(likeNumber))
            #get comment
            commentElement = elementPost.find_element_by_xpath(
                ".//div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/div/span")
            commentNumber = commentElement.get_attribute('innerHTML')
            print("commentNumber: {}".format(commentNumber))
            #get text content
            try:
                textContainElement = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[1]/div/div/div/span/div/div")
                textContain = cleanhtml(textContainElement.get_attribute('innerHTML'))
                print("textContain: {}".format(textContain))
            except Exception as ex:
                pass
            #get image content
            try:
                imagePostElement = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[2]/div[1]/div/div/div/div/div/div[1]/div/div/div[1]/div/a/div[1]/div[1]/div/img")
                imagePost = unescape(imagePostElement.get_attribute('src'))
                print("imagePost: {}".format(imagePost))
            except Exception as ex:
                pass
            #is that a video
            try:
                VideoElement = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div[2]/div/div[contains(@role,'presentation')]")
                print("Video")
            except Exception as ex:
                pass
            #share post owner infor
            try:
                sharePostOwnerElement = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[2]/div/div/div[2]/div/div/div[1]/span/h3/span[1]/a/strong/span")
                sharePostOwner = sharePostOwnerElement.get_attribute('innerHTML')
                print("sharePostOwner: {}".format(sharePostOwner))
            except Exception as ex:
                pass
            #share post image infor
            try:
                imageSharePost = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/a/div[1]/div[1]/div/img")
                imageLink = unescape(imageSharePost.get_attribute('src'))
                print("imageLink Share: {}".format(imageLink))
            except Exception as ex:
                pass
            #share post text content
            try:
                contentSharePostElement = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[2]/div/div/div[3]/div/div/div/div/span/div/div[1]")
                contentSharePost = cleanhtml(contentSharePostElement.get_attribute('innerHTML'))
                print("contentSharePost: {}".format(contentSharePost))
            except Exception as ex:
                pass
            #share post video owner
            try:
                videoShareOwnerElement = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[2]/div[2]/div/a/div/div/div[1]/div[1]/span/span")
                videoShareOwner = cleanhtml(videoShareOwnerElement.get_attribute('innerHTML'))
                print("videoShareOwner: {}".format(videoShareOwner))

                videoTitleSharedElement = elementPost.find_element_by_xpath(
                    ".//div[2]/div/div[3]/div[2]/div[2]/div/a/div/div/div[1]/div[2]/div/div[1]/span/span/span")
                videoTitleShared = cleanhtml(videoTitleSharedElement.get_attribute('innerHTML'))  
                print("videoTitleShared: {}".format(videoTitleShared))  
            except Exception as ex:
                pass           
            print("________________________________________")

        print("Success get emelent")
    except Exception as ex:
        print('Error get element post:{}'.format(ex))

def getDetailPostFace(driver, link):   
    time.sleep(2) 
    driver.get(link)
    print('get data' + driver.title)
    try:
        if link.find("posts") != -1:
            print("Get detail for post")
            try:     
                try:   
                    # try to get post detail 1
                    elementPostDetail = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div")))
                except Exception as ex:
                    # try to get post detail 2
                    elementPostDetail = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div")))
                #get title            
                elementTitle = elementPostDetail.find_element_by_xpath(".//strong/span")
                title = elementTitle.get_attribute('innerHTML')
                print("title:{}".format(title))
                #get time
                elementTime = elementPostDetail.find_element_by_xpath(".//span/b")
                timePost = elementTime.find_element_by_xpath(".//b[not(@style)]").get_attribute('innerHTML')
                print("timePost:{}".format(timePost))
                #content
                elementContent = elementPostDetail.find_element_by_xpath("./div[3]/div[1]/div/div/div/span")
                content = cleanhtml(elementContent.get_attribute('innerHTML'))
                print("content:{}".format(content))
                #like
                elementLike = elementPostDetail.find_element_by_xpath("./div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span")
                like = elementLike.get_attribute('innerHTML')
                print("like number:{}".format(like))
                #comment
                elementComment = elementPostDetail.find_element_by_xpath("./div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/div/span")
                comment = elementComment.get_attribute('innerHTML')
                print("comment number:{}".format(comment))
                #share
                elementShare = elementPostDetail.find_element_by_xpath("./div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[2]/span/div/span")
                share = elementShare.get_attribute('innerHTML')
                print("share number:{}".format(share))
            except Exception as ex:
                print("Get detai post error:{}".format(ex))

        elif link.find("watch") != -1:
            print("Get detail for watch")
            try:        
                # try to get post detail
                elementPostDetail = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/div/div[2]/div[1]")))
                #get title            
                elementTitle = elementPostDetail.find_element_by_xpath(".//strong/span")
                title = elementTitle.get_attribute('innerHTML')
                print("title:{}".format(title))
                #get time
                elementTime = elementPostDetail.find_element_by_xpath(".//span/b")
                timePost = elementTime.find_element_by_xpath(".//b[not(@style)]").get_attribute('innerHTML')
                print("timePost:{}".format(timePost))
                #content
                elementContent = elementPostDetail.find_element_by_xpath("./div[2]/div/div[1]/span/div/div")
                content = cleanhtml(elementContent.get_attribute('innerHTML'))
                print("content:{}".format(content))
                #like
                elementLike = driver.find_element_by_xpath("//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/span/span/span")
                like = elementLike.get_attribute('innerHTML')
                print("like number:{}".format(like))
                #comment
                elementComment = driver.find_element_by_xpath("//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div/div[3]/div/span")
                comment = elementComment.get_attribute('innerHTML')
                print("comment number:{}".format(comment))
                #views
                elementView = driver.find_element_by_xpath("//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div/span/span")
                view = unescape(elementView.get_attribute('innerHTML'))
                print("view number:{}".format(view))
            except Exception as ex:
                print('Error post detail:{}'.format(ex))
        elif link.find("videos") != -1:
            print("Get detail for video")
            try:        
                # try to get post detail
                elementPostDetail = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div")))
                #get title            
                elementTitle = elementPostDetail.find_element_by_xpath(".//strong/span")
                title = elementTitle.get_attribute('innerHTML')
                print("title:{}".format(title))
                #get time
                elementTime = elementPostDetail.find_element_by_xpath(".//span/b")
                timePost = elementTime.find_element_by_xpath(".//b[not(@style)]").get_attribute('innerHTML')
                print("timePost:{}".format(timePost))
                #content
                elementContent = elementPostDetail.find_element_by_xpath("./div[1]/div[2]/div[2]/div/span/div/div")
                content = cleanhtml(elementContent.get_attribute('innerHTML'))
                print("content:{}".format(content))
                #like
                elementLike = elementPostDetail.find_element_by_xpath("./div[2]/div[1]/div/div[1]/div/span/div/span[2]/span/span")
                like = elementLike.get_attribute('innerHTML')
                print("like number:{}".format(like))
                #comment
                elementComment = elementPostDetail.find_element_by_xpath("./div[2]/div[1]/div/div[2]/div[1]/div/span")
                comment = elementComment.get_attribute('innerHTML')
                print("comment number:{}".format(comment))
                #views
                elementView = elementPostDetail.find_element_by_xpath("./div[2]/div[1]/div/div[2]/div[2]/span/span")
                view = unescape(elementView.get_attribute('innerHTML'))
                print("view number:{}".format(view))
            except Exception as ex:
                print('Error post detail:{}'.format(ex))


    except Exception as ex:
        print('Error get element post detail:{}'.format(ex))

def getDataFace(driver, nameSearch):
    print('get data' + driver.title)
    CONT = Facebook()
    driver.get("https://www.facebook.com/" + nameSearch)
    try:
        try:
            # try to get fanpage group name
            elementFanpageName = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, CONT.fanpageGroupName)))
            name = elementFanpageName.get_attribute('innerHTML')
            print(name)
            elementFanpageMember = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, CONT.fanpageGroupMember)))
            member = elementFanpageMember.get_attribute('innerHTML')
            print(member)
        except Exception as ex:
            try:
                # try to get fanpage
                elementFanpage = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.fanpageImage)))
                image = elementFanpage.get_attribute('innerHTML')
                start = image.find("https://")
                end = image.find("></image>")
                image = image[start:end-1]
                image = unescape(image)
                print(image)
                elementFanpageName = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.fanpageName)))
                name = elementFanpageName.get_attribute('innerHTML')
                print(name)

            except Exception as ex:
                # get image and name of user
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.userImage)))
                image = element.get_attribute('innerHTML')
                start = image.find("https://")
                end = image.find("></image>")
                image = image[start:end-1]
                image = unescape(image)
                name = element.get_attribute('aria-label')
                print(name)
                print(image)
                try:
                    elementFollower = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, CONT.userFollower)))
                    follower = elementFollower.get_attribute('innerHTML')
                    print(follower)
                except Exception as ex:
                    print("Do not have follwer")
    except Exception as ex:
        print(ex)


def getInfoIntagram(driver, nameSearch):
    print('get data' + driver.title)
    CONT = Intagram()
    driver.get("https://www.instagram.com/" + nameSearch)
    try:
        try:
            elementImage = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, CONT.xpathImage)))
            image = elementImage.get_attribute('src')
            print(image)
            elementName = driver.find_element_by_xpath(CONT.xpathName)
            name = elementName.get_attribute('innerHTML')
            print(name)
            elementInformations = driver.find_element_by_xpath(CONT.xpathInfo)
            elementInfos1 = elementInformations.find_elements_by_xpath(
                "./li/span")
            elementInfos2 = elementInformations.find_elements_by_xpath(
                "./li/a")
            for elementInfo1 in elementInfos1:
                print(cleanhtml(elementInfo1.get_attribute('innerHTML')))
            for elementInfo2 in elementInfos2:
                print(cleanhtml(elementInfo2.get_attribute('innerHTML')))
        except Exception as ex:
            print("Error get info {}".format(ex))
    except Exception as ex:
        print(ex)

def getInstagramPostDetail(driver, linkPost):
    print('get data' + driver.title)
    print("link post:{}".format(linkPost))
    driver.get(linkPost)
    try:
        authorElement = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,"//body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div/span/a")))
        author = authorElement.get_attribute('innerHTML')
        print("author:{}".format(author))

        numLikeElement = driver.find_element_by_xpath("//body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a")
        numLike = cleanhtml(numLikeElement.get_attribute('innerHTML'))
        print("numLike:{}".format(numLike))

        try:
            contentElement = driver.find_element_by_xpath("//body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span")
            content = cleanhtml(contentElement.get_attribute('innerHTML'))
            print("Content:{}".format(content))
        except Exception as ex:
            pass

        print("-------------------")        
        commentElements = driver.find_elements_by_xpath("//body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul")
        #expand all reply
        for commentElement in commentElements:
            try:
                replyElement = commentElement.find_element_by_xpath("./li/ul/li/div/button/span")
                action = ActionChains(driver)     
                scroll_shim(driver,replyElement)
                time.sleep(2)
                action.move_to_element(replyElement).perform()                    
                replyElement.click()
                time.sleep(2)
            except Exception as ex:
                pass
    
        commentElements2 = driver.find_elements_by_xpath("//body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul")
        #get all data comment
        for commentElement in commentElements2:
            try:
                commentOwnerElement = commentElement.find_element_by_xpath(".//h3/div/span/a")
                commentOwner = commentOwnerElement.get_attribute('innerHTML')
                print("commentOwner:{}".format(commentOwner))
                commentDetailElement = commentElement.find_element_by_xpath("./div/li/div/div[1]/div[2]/span")
                commentDetail = commentDetailElement.get_attribute('innerHTML')
                print("commentDetail:{}".format(commentDetail))

                #get replay
                try:                
                    replyDetails = commentElement.find_elements_by_xpath("./li/ul/div")
                    for replyDetail in replyDetails:                    
                        replyOwnerElement = replyDetail.find_element_by_xpath(".//h3/div/span/a")
                        replyOwner = replyOwnerElement.get_attribute('innerHTML')
                        print("----replyOwner:{}".format(replyOwner))
                        replyContentElement = replyDetail.find_element_by_xpath("./li/div/div[1]/div[2]/span")
                        replyContent = cleanhtml(replyContentElement.get_attribute('innerHTML'))
                        print("----replyContent:{}".format(replyContent))
                except Exception as ex:
                    print("except:{}".format(ex))
                print("-------------------")
                
            except Exception as ex:
                pass

        
    except Exception as ex:
        print("UnHandle except: {}".format(ex))
    

def getInstagramPost(driver, nameImsta):
    print('get data' + driver.title)
    driver.get("https://www.instagram.com/" + nameImsta)
    try:
        isExist = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,"//body/div[1]/section/main/div/div[3]/article/div[1]/div/div/div")))
        elementPosts = driver.find_elements_by_xpath("//body/div[1]/section/main/div/div[3]/article/div[1]/div/div/div")
        
        for elementPost in elementPosts:
            scroll_shim(driver,elementPost)
            time.sleep(2)       
            action = ActionChains(driver)     
            action.move_to_element(elementPost).perform()
            time.sleep(2)
            # get like
            likeElement = elementPost.find_element_by_xpath("./a/div/ul/li[1]/span[1]")
            like = likeElement.get_attribute('innerHTML')
            print("like: {}".format(like))
            # get comment
            commentElement = elementPost.find_element_by_xpath("./a/div/ul/li[2]/span[1]")
            comment = commentElement.get_attribute('innerHTML')
            print("comment: {}".format(comment))
            # get image
            imageElement = elementPost.find_element_by_xpath(".//img")
            image = unescape(imageElement.get_attribute("src"))
            print("image: {}".format(image))
            # get link
            elementPost.click()
            try:
                closeElement = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,"/html/body/div[5]/div[3]/button")))
                print("link post: {}".format(driver.current_url))
                time.sleep(2)
                closeElement.click()
            except Exception as ex:
                pass

    except Exception as ex:
        print("UnHandle except: {}".format(ex))

