class youtubeConstant:
    xpathAbout = '//ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[6]'
    xpathName = '//*[@id="channel-header"]//div[@id="inner-header-container"]//yt-formatted-string[@class="style-scope ytd-channel-name"]'
    xpathSubscriber = '//*[@id="channel-header"]//div[@id="inner-header-container"]//yt-formatted-string[@id="subscriber-count"]'
    xpathImage = '//*[@id="channel-header"]//yt-img-shadow[@id="avatar"]//img'
    xpathCover = '//*[@id="banner-editor"]'
    xpathDescription = '//yt-formatted-string[@id="description"]'
    xpathAllVideo = '//ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[2]'
    xpathVideos = '//div[@id="items" and @class="style-scope ytd-grid-renderer"]/ytd-grid-video-renderer'
    xpathTime = '//div[@id="info-strings"]//yt-formatted-string'
    xpathComment = '//ytd-comments/ytd-item-section-renderer//ytd-comments-header-renderer//yt-formatted-string/span[1]'
    xpathView = '//div[@id="info-text"]//ytd-video-view-count-renderer/span[1]'
    xpathHashTag = '//div[contains(@class,"ytd-video-primary-info-renderer")]//a[contains(@href,"hashtag") and not(@hidden)]'