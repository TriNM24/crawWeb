class Facebook:
    xpathEmail = '//*[@id="email"]'
    xpathPass = '//*[@id="pass"]'
    xpathSubmit = '/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]'
    facebookUser = '0582004489'
    facebookPass = 'HaoThien1991'
    searchBox = '/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div/div/div/div/div/label/input'
    # nameSearch = 'tri.nguyen.73'
    # nameSearch = 'tuanva186'
    # nameSearch = 'fanfanoutdoor'
    # nameSearch = 'groups/2306051969426578'
    nameSearch = 'ngoctrinhfashion89'
    fanpageGroupName = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/h1/span"
    fanpageGroupMember = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/span/div/div[3]"
    fanpageImage = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[1]//*[local-name() = 'svg']"
    fanpageName = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div[1]/h2/span/span"

    userImage = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]//*[local-name() = 'svg']"
    userFollower = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[1]/div[2]/div/div[2]/span/span/a"


class Intagram:
    xpathMail = '//main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input | //main/div/div/div[1]/div/form/div/div[1]/div/label/input'
    xpathPass = '//main/div/div/div[1]/div/form/div/div[2]/div/label/input | //main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input'
    xpathButtonLogin = '//main/div/div/div[1]/div/form/div/div[3] | //main/article/div[2]/div[1]/div/form/div/div[3]'
    notNowButtonSaveInfo = "//body/div[1]/section/main/div/div/div/div/button"
    notNowButtonNotification = "//body/div[4]/div/div/div/div[3]/button[2]"
    xpathAcceptAll = "//button[text()='Accept All']"
    userName = 'nguyenminhtri644'
    passWord = "Tri123456"
    cookies_file = "cookies_integram.pkl"
    nameSearch = 'khloekardashian'
    xpathImage = "/html/body/div[1]/section/main/div/header/div/div/span/img"
    xpathName = "/html/body/div[1]/section/main/div/header/section/div[1]/h2"
    xpathInfo = "/html/body/div[1]/section/main/div/header/section/ul"
    defautWait = 5
