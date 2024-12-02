import requests

url = "https://www.youtube.com/youtubei/v1/subscription/subscribe?prettyPrint=False"
headers = {
    "Host": "www.youtube.com",
    "cookie": "YSC=XvBHZtbMPD4; VISITOR_INFO1_LIVE=SLsnLZMalOc; VISITOR_PRIVACY_METADATA=CgJWThIEGgAgGg%3D%3D; PREF=f4=4000000&f6=40000000&tz=Asia.Saigon; SID=g.a000qwi6ZUakxCfAoyyh8WmLfUau27jSiNHryTRKFIPPuClOPFCcUgpT81RXLYJGzisi_glWlgACgYKAQESARcSFQHGX2MipvhYZqyR1HNFMeJSMrhP1hoVAUF8yKoToUZ9WYkzZwYmkHmanvm20076; __Secure-1PSIDTS=sidts-CjEBQT4rX5SgIEXq8DCwh7czBXZ9lqmfivAuRstmJfxrjZJ1b6_Yutm7JtZizjGo5FWKEAA; __Secure-3PSIDTS=sidts-CjEBQT4rX5SgIEXq8DCwh7czBXZ9lqmfivAuRstmJfxrjZJ1b6_Yutm7JtZizjGo5FWKEAA; __Secure-1PSID=g.a000qwi6ZUakxCfAoyyh8WmLfUau27jSiNHryTRKFIPPuClOPFCcXranH2aLiPZA7mkJMLtBhAACgYKAXISARcSFQHGX2Mi1T1E5o0khufmkEi9By8ztRoVAUF8yKoSpJQ4h-V2HJoD_DhNnVnd0076; __Secure-3PSID=g.a000qwi6ZUakxCfAoyyh8WmLfUau27jSiNHryTRKFIPPuClOPFCcrSCe1TLt2TUz3nFUtQFVPQACgYKATESARcSFQHGX2Mi63qWJ2T9vXpx2GLvLSKMqBoVAUF8yKq8cYgyn3IEt9clj2_Nb9Xx0076; HSID=AV6fIidC2sHd2tMK0; SSID=AkdnQsuFrWQ1O-KNM; APISID=NmS2IE71EhrGr8qr/AewpGCcrR9VTr4U7t; SAPISID=tg3XaRLLrWJdZ-tZ/ADVChlVRRw22MRDBa; __Secure-1PAPISID=tg3XaRLLrWJdZ-tZ/ADVChlVRRw22MRDBa; __Secure-3PAPISID=tg3XaRLLrWJdZ-tZ/ADVChlVRRw22MRDBa; LOGIN_INFO=AFmmF2swRQIgULjT8DtPHOO9CeQXCB-04-YWQqnVEpynOS0_DZZ-tOICIQCdY3NrcZVX6qt-VWUaZbb1PstKTqUI24DtZdoQYGLPLw:QUQ3MjNmemtuZGttdnFTN1ZJVHFuU3c5dWhRRFZEOU51RWJ0cVZjV3hfQTJUdFpYaTNxUkt4NHhPVDFDV2ZRZzQ1LWxJY3g4X2c0ZEh0T3RNQm04aG9KbzNmcVFfZlBLMWpocURtb3FjR2p4UUNoMmZlOWtfT2VCUloyeUsybHctUVIxZFdVQU9Kak9rWW1wWEFKSExxYjNxZlUxeVZXcmJB; SIDCC=AKEyXzXC2QqyZ9tAAWuiLTC07OWUnQY7qzCRIEY76MOLwSBK1Tx-3b6P1iVE-28y6idaTtSu8u8; __Secure-1PSIDCC=AKEyXzVAQkwOcx-8fsgF7hh8ZBRTeJvo2XCWGd0M8f0CFbLJFLey9ZF5IAdq3PBmnIj8Stm8PN8; __Secure-3PSIDCC=AKEyXzVDlS3Hau7KhiRdMlp_K2PSRMJ3Af_BIMBXHbJlceX7jH6NM2ARoEnGAtKGhdEuNa1Cv3w; CONSISTENCY=AKreu9umw_R_zltsi2wwYQdFEWSAYc_kIiAxNxRSneBdrLMrnRqQbnRUokGy25KK4YYNGpehxRrkq8l0s0O162MEAtI0XNgDCy-C9SzBI-GD58vT9EwfVfUwYVQ; ST-1b=itct=CHkQ8KgHGAAiEwj9-cH5vYGKAxUFSfUFHYlOK48%3D&csn=Cq_nlF-Xu1CsnDSz&session_logininfo=AFmmF2swRQIgULjT8DtPHOO9CeQXCB-04-YWQqnVEpynOS0_DZZ-tOICIQCdY3NrcZVX6qt-VWUaZbb1PstKTqUI24DtZdoQYGLPLw%3AQUQ3MjNmemtuZGttdnFTN1ZJVHFuU3c5dWhRRFZEOU51RWJ0cVZjV3hfQTJUdFpYaTNxUkt4NHhPVDFDV2ZRZzQ1LWxJY3g4X2c0ZEh0T3RNQm04aG9KbzNmcVFfZlBLMWpocURtb3FjR2p4UUNoMmZlOWtfT2VCUloyeUsybHctUVIxZFdVQU9Kak9rWW1wWEFKSExxYjNxZlUxeVZXcmJB&endpoint=%7B%22clickTrackingParams%22%3A%22CHkQ8KgHGAAiEwj9-cH5vYGKAxUFSfUFHYlOK48%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2F%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_BROWSE%22%2C%22rootVe%22%3A3854%2C%22apiUrl%22%3A%22%2Fyoutubei%2Fv1%2Fbrowse%22%7D%7D%2C%22browseEndpoint%22%3A%7B%22browseId%22%3A%22FEwhat_to_watch%22%7D%7D; ST-yve142=session_logininfo=AFmmF2swRQIgULjT8DtPHOO9CeQXCB-04-YWQqnVEpynOS0_DZZ-tOICIQCdY3NrcZVX6qt-VWUaZbb1PstKTqUI24DtZdoQYGLPLw%3AQUQ3MjNmemtuZGttdnFTN1ZJVHFuU3c5dWhRRFZEOU51RWJ0cVZjV3hfQTJUdFpYaTNxUkt4NHhPVDFDV2ZRZzQ1LWxJY3g4X2c0ZEh0T3RNQm04aG9KbzNmcVFfZlBLMWpocURtb3FjR2p4UUNoMmZlOWtfT2VCUloyeUsybHctUVIxZFdVQU9Kak9rWW1wWEFKSExxYjNxZlUxeVZXcmJB",
    "Authorization": "SAPISIDHASH 1732881490_5b9a227b417ebc2f9ebd0741e2de2114ede3b0d4_u SAPISID1PHASH 1732881490_5b9a227b417ebc2f9ebd0741e2de2114ede3b0d4_u SAPISID3PHASH 1732881490_5b9a227b417ebc2f9ebd0741e2de2114ede3b0d4_u",
    "Sec-Ch-Ua": "\"Not?A_Brand\";v=\"99\", \"Chromium\";v=\"130\"",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Ch-Ua-Bitness": "",
    "Sec-Ch-Ua-Model": "",
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Youtube-Client-Name": "1",
    "Sec-Ch-Ua-Wow64": "?0",
    "X-Origin": "https://www.youtube.com",
    "X-Youtube-Client-Version": "2.20241126.01.00",
    "Sec-Ch-Ua-Arch": "",
    "Sec-Ch-Ua-Full-Version": "",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Form-Factors": "",
    "X-Youtube-Bootstrap-Logged-In": "true",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Goog-Visitor-Id": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
    "X-Goog-Authuser": "0",
    "Sec-Ch-Ua-Platform-Version": "",
    "Accept": "*/*",
    "Origin": "https://www.youtube.com",
    "X-Client-Data": "CPyRywE=",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "same-origin",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.youtube.com/@AnimeWiki/videos",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
  }

data = """{"context":{"client":{"hl":"vi","gl":"VN","remoteHost":"14.168.129.34","deviceMake":"","deviceModel":"","visitorData":"","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.61 Chrome/126.0.6478.61 Not/A)Brand/8  Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20241126.01.00","osName":"Windows","osVersion":"10.0","originalUrl":"","screenPixelDensity":1,"platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{},"screenDensityFloat":1.25,"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","timeZone":"Asia/Saigon","browserName":"Chrome","browserVersion":"126.0.6478.61","acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","deviceExperimentId":"","screenWidthPoints":982,"screenHeightPoints":703,"utcOffsetMinutes":420,"connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"4000000","mainAppWebInfo":{"graftUrl":"","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":true}},"user":{"lockedSafetyMode":false},"request":{"useSsl":true,"consistencyTokenJars":[{"encryptedTokenJarContents":""}],"internalExperimentFlags":[]},"clientScreenNonce":"Q7Y2oPEJDR59zgp2","clickTracking":{"clickTrackingParams":""},"adSignalsInfo":{"params":[{"key":"dt","value":"1732875842328"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"420"},{"key":"u_his","value":"19"},{"key":"u_h","value":"864"},{"key":"u_w","value":"1536"},{"key":"u_ah","value":"824"},{"key":"u_aw","value":"1536"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"703"},{"key":"biw","value":"965"},{"key":"brdim","value":"0,0,0,0,1536,0,1536,824,982,703"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}],"bid":"ANyPxKos1T8b8S3EKi7Jqh5V_L1XggslFqI7k1jecuK8mzRtHcSuxqADsL3hFZxXQ3JdHlsQP2S8lui6jBGj5sLS05NR0g_ALw"}},"channelIds":["UC6kN3WEmUdv-5SzhY_TerOA"],"params":""}"""
r = requests.post(
    url=url,
    headers=headers,
    data=data
)

print(r.status_code, r.text)