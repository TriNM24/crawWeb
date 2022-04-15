class tiktokConstant:
    cookies_file = 'tiktokCookies.pkl'
    userName = 'tri_nguyen833'
    password = 'Test@123456'
    xpathCloseVerify = '//*[@id="verify-bar-close"]'
    # xpathName = '//body/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/h1 | //body/div[1]/div/div[2]/div[2]/div/header/div[1]/div[2]/h1/span | //body/div/div/div[2]/div[2]/div/header/div[1]/div[2]/h1/span | //body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]/h2 | //body//h2[@data-e2e="user-title"] | //body//h1[@data-e2e="user-title"]'
    xpathName = '//body//h2[@data-e2e="user-title"] | //body//h1[@data-e2e="user-title"]'
    # xpathInfos = '//body/div[1]/div[2]/div[2]/div/div[1]/h2[1] | //body/div[1]/div/div[2]/div[2]/div/header/h2[1] | //body/div[2]/div[2]/div[2]/div/div[1]/h2[1] | //body//div[contains(@class,"ShareLayoutHeader")]/h2[contains(@class,"CountInfos")]'
    xpathInfos = '//body//div[contains(@class,"ShareLayoutHeader")]/h2[contains(@class,"CountInfos")]'
    # xpathImage = '//body/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/span/img | //body/div[1]/div/div[2]/div[2]/div/header/div[1]/div[1]/span/img | //body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/span/img | //body//div[@data-e2e="user-avatar"]/span/img[contains(@class,"ImgAvatar")]'
    xpathImage = '//body//div[@data-e2e="user-avatar"]/span/img[contains(@class,"ImgAvatar")]'
    # xpathDescription = '//body/div/div/div[2]/div[2]/div/header/h2[2] | //body/div[1]/div[2]/div[2]/div/div[1]/h2[2] | //body/div[2]/div[2]/div[2]/div/div[1]/h2[2] | //body//h2[@data-e2e="user-bio"]'
    xpathDescription = '//body//h2[@data-e2e="user-bio"]'

    xpathVideos = '//main//div[contains(@class,"video-feed-item")] | //body//div[contains(@class,"DivItemContainer")]'