import requests
import colorama
import random
colorama.init()

# make color for logs
def error_color(string: str):
    return colorama.Fore.RED + str(string) + colorama.Style.RESET_ALL
def success_color(string: str):
    return colorama.Fore.GREEN + str(string) + colorama.Style.RESET_ALL
def system_color(string: str):
    return colorama.Fore.YELLOW + str(string) + colorama.Style.RESET_ALL
def wait_color(string: str):
    return colorama.Fore.BLUE + str(string) + colorama.Style.RESET_ALL
def purple_color(string: str):
    return colorama.Fore.MAGENTA + str(string) + colorama.Style.RESET_ALL

# instagram headers
INSTAGRAM_HEADER = {
        "authority": "www.instagram.com",
        "method": "POST",
        "path": "/graphql/query",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "us",
        "content-length": "1303",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "", # cookies instagram (add later)
        "origin": "https://www.instagram.com",
        "priority": "u=1, i",
        "referer": "https://www.instagram.com/truonhfrus/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"8.0.0\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "x-asbd-id": "129477",
        "x-bloks-version-id": "d064162f4a1bc5cbc2a7ce44dd98b555613e0264ce1d0ebd6be60a79d3c58f44",
        "x-csrftoken": "", # csrftoken (add later)
        "x-fb-friendly-name": "PolarisAPIGetFrCookieQuery",
        "x-fb-lsd": "gtE021O5IF-2TGA5JwktM8",
        "x-ig-app-id": "936619743392459"
    }
# instagram requests follow payloads
INSTAGRAM_DATA = {
        "av": "17841469559245655",
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "__req": "22",
        "__hs": "19999.HYP:instagram_web_pkg.2.1..0.1",
        "dpr": "1",
        "__ccg": "UNKNOWN",
        "__rev": "1017023141",
        "__s": "4qko6i:p7ocnq:i4baiu",
        "__hsi": "7421468926897011504",
        "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o1DU2_CwjE1xoswaq0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo31w9a9wtUd8-U2zxe2GewGw9a361qw8Xxm16wUwtEvw5rCwLyESE7i3vwDwHg2ZwrUdUbGwmk0zU8oC1Iwqo5q3e3zhA6bwIDyUrAwCAxW1oCz8rwHwjE7SEy",
        "__csr": "gH132kn2c5tgx5s9Oi9RshbASGhii4hbQSrnnKSVd96qhfBiryVrTnLAqp5QGLBgCinHVJ8y_GiVkamp3bBJGVX88y4Ah7rpk8AyeQ7bBxipGvAU8oJ-GxaFEpJu9Cqh9KEyECiqmhu-fCwxzUqx200jjt0hS788qhqwpoIE27wlU1v48g1PU37cbwAo9o-4Q1ggShwGwdm07PFJ0da08ewad0gAU9o66hPG4k2e210r84rIE5ABpR20lx62ySqmpo2DzEhxje0N6mkE2Cpo5q1GhUK2V08e9wmo2cwh84I4M-Kfwj8fU5e02VG01cmw1rW",
        "__comet_req": "7",
        "fb_dtsg": "NAcMaVzpqfNdw85WUWDU_-mFYIudkks48C3vioXyzW8vt2WAGhrmi5A:17843683195144578:1727945385",
        "jazoest": "26434",
        "lsd": "VoKNH81gy4VZlD1--Q4woP",
        "__spin_r": "1017023141",
        "__spin_b": "trunk",
        "__spin_t": "1727945387",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "usePolarisFollowMutation",
        "variables": "{\"target_user_id\":\"65635471598\",\"container_module\":\"profile\",\"nav_chain\":\"PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected\"}",
        "server_timestamps": "true",
        "doc_id": "7275591572570580"
    }
# instagram user agents (for random)
INSTAGRAM_USER_AGENT = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0."
    ]



# get random proxy working
def get_proxies():
    proxy = None
    while True:
        print(colorama.Fore.BLUE + f"đang lấy proxy cho follow instagram..." + colorama.Style.RESET_ALL)
        try:
            get_proxy = requests.get(
                    url="https://gimmeproxy.com/api/getProxy",
                )
            proxy = f"http://{get_proxy.json()['ip']}:{get_proxy.json()['port']}"
            test_proxy = requests.get(
                url="https://google.com/",
                proxies={"http": proxy},
                timeout=2
            )
            if test_proxy.status_code == 200:
                break
            else:
                continue
        except:
            continue
    print(colorama.Fore.GREEN + f"đã lấy proxy {proxy} thành công!" + colorama.Style.RESET_ALL)
    return proxy



# following instagram target
def follow_instagram(insta_link, object_id, cookies: str, proxy: bool = True):
    global INSTAGRAM_DATA
    global INSTAGRAM_HEADER
    # get x-csrftoken from string cookies and add it in headers
    INSTAGRAM_HEADER["x-csrftoken"] = cookies.split("csrftoken=")[1].split(";")[0]
    INSTAGRAM_HEADER['cookie'] = cookies # add cookies in headers
    INSTAGRAM_HEADER['referer'] = insta_link # add target instagram link on headers
    INSTAGRAM_HEADER['user-agent'] = random.choice(INSTAGRAM_USER_AGENT) # add random user agent in headers
    INSTAGRAM_DATA["variables"] = ('{'f'"target_user_id": "{object_id}",''"container_module": "profile",''"nav_chain": "PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected"''}')
    print(wait_color("đang thực hiện kiểm tra tài khoản instagram mục tiêu..."))
    
    if proxy:
        proxies = {'http': get_proxies()}
    else:
        proxies = None
        
    try:
        response = requests.post(
            url="https://www.instagram.com/graphql/query",
            headers=INSTAGRAM_HEADER,
            data=INSTAGRAM_DATA,
            proxies=proxies
        )
        insta_json_res = response.json()['data']["xdt_create_friendship"]["friendship_status"]
        return {"following_status": insta_json_res["following"], "outgoing_request": insta_json_res['outgoing_request']}
    # can inference None type error is this target is not found
    except TypeError as e:
        print(f"lỗi follow instagram: {e}")
        return {"page_not_found": "trang instagram này không tồn tại!"}
    # unknow error
    except Exception as e:
        print(f"lỗi follow instagram: {e}")
        return {'error': True}