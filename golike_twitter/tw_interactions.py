import requests
import colorama
import json
import random
import os
colorama.init()

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

headers = {
  "authority": "x.com",
  "method": "POST",
  "path": "/i/api/1.1/friendships/create.json",
  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
  "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
  "content-length": "306",
  "content-type": "application/x-www-form-urlencoded",
  "cookie": "", # add later in code
  "origin": "https://x.com",
  "priority": "u=1, i",
  "referer": "", # add later in code
  "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
  "x-client-transaction-id": "jRl287bDW1N1cOL7VOPwmTzLNkcHHFYbPXKOdvzkA34aSgphBzhK0HFgpo/Rs7H7g1IARI9GSNJraXTqmZ5D0LskCjS9jg",
  "x-client-uuid": "cfca0c29-831a-4039-b664-edaf45cbd7ee",
  "x-csrf-token": "", # add later in code
  "x-twitter-active-user": "yes",
  "x-twitter-auth-type": "OAuth2Session",
  "x-twitter-client-language": "vi"
}

follow_payloads = {
  "include_profile_interstitial_type": 1,
  "include_blocking": 1,
  "include_blocked_by": 1,
  "include_followed_by": 1,
  "include_want_retweets": 1,
  "include_mute_edge": 1,
  "include_can_dm": 1,
  "include_can_media_tag": 1,
  "include_ext_is_blue_verified": 1,
  "include_ext_verified_type": 1,
  "include_ext_profile_image_shape": 1,
  "skip_status": 1,
  "user_id": "" # add later in code
}

url = "https://x.com/i/api/1.1/friendships/create.json"

# instagram user agents (for random)
if not os.path.exists("./ua.json"):
    input(print(colorama.Fore.YELLOW + "[!] chưa có tệp 'ua.json' để hoạt động, enter để tạo\n-> " + colorama.Style.RESET_ALL))
    obj = {
        "__comment": "bạn có thể thêm vào cho list UA (User Agent) bên dưới (UA của máy đang đăng nhập tài khoản instagram)",
        "UA": []
    }
    with open("./ua.json", "w") as file:
        json.dump(obj, file)
    input(print(colorama.Fore.YELLOW + "[!] vui lòng vào tệp 'ua.json' để thiết lập, enter để đóng\n-> " + colorama.Style.RESET_ALL))
    exit()

with open("./ua.json", "r") as file:
    ua = json.load(file)
if str(ua['UA']) == "[]":
    input(print(colorama.Fore.YELLOW + "[!] vui lòng vào tệp 'ua.json' để thiết lập, enter để đóng\n-> " + colorama.Style.RESET_ALL))
    exit()

TWITTER_USER_AGENT = ua['UA']

# get random proxy working
def get_proxies():
    proxy = None
    while True:
        print(colorama.Fore.BLUE + f"đang lấy proxy cho follow twitter..." + colorama.Style.RESET_ALL)
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


# follow twitter
def __follow(cookie: str, target_id: int, target_link: str, proxy: bool = True, username=None, twitter_cookies_path="twitter_cookies.json"):
    headers['user-agent'] = random.choice(TWITTER_USER_AGENT)
    
    # load old cookies storaged in file
    if os.path.exists(twitter_cookies_path):
        with open(twitter_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load and proxy:
            if cookies_load[username]['cookie'] != "":
                cookie = cookies_load[username]['cookie']

    if proxy:
        proxies = {"http": get_proxies()}
    else:
        proxies = None

    headers['cookie'] = cookie
    headers['x-csrf-token'] = cookie.split("ct0=")[1].split(";")[0]
    follow_payloads['user_id'] = target_id
    headers['referer'] = target_link
    try:
        response = requests.post(
                url=url,
                headers=headers,
                data=follow_payloads,
                proxies=proxies
            )
        response = requests.post(
                url=url,
                headers=headers,
                data=follow_payloads,
                proxies=proxies
            )
        response_json = response.json()
        if "errors" in response_json:
            response_json['status_code'] = response.status_code
            return response_json
        elif "following" in response_json:
            response_json = {"target": target_link, "following": response_json['following']}
            response_json['status_code'] = response.status_code
            return response_json
        else:
            return {"error": "lỗi không xác định"}
    except Exception as e:
        return {"error": f"đã có lỗi, mã lỗi: {e}"}
    

def tw_follow(cookie: str, target_id: int, target_link: str, proxy: bool = True, username=None, max_try=1):
    follow_output = {"error": "empty"}
    for i in range(max_try):
        follow_output = __follow(cookie, target_id, target_link, proxy)
        if "error" in follow_output or "errors" in follow_output:
            print(error_color(f"[!] lỗi khi follow, thử lại, lân thử -> {i+1}/{max_try}"))
        else:
            break
    return follow_output