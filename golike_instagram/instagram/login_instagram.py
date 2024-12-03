import time
import requests
import colorama
import random
import os
import json
from instagram_interection import follow_instagram
from pass_verify_automation import pass_verify_automation
from pass_captcha import PassInstagramCaptcha, captcha_dectect
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


INSTAGRAM_USER_AGENT = ua['UA']
ERR = False
CSRF_TOKEN = None
COOKIE = None

# headers have csrf token and random UA
headers = {
    "User-Agent": "",
    "authority": "www.instagram.com",
    "method": "GET",
    "path": "/",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "vi",
    "cache-control": "max-age=0",
    "cookie": 'wd=954x746; dpr=1.25',
    "dpr": "1.25",
    "priority": "u=0, i",
    "referer": "https://www.instagram.com/accounts/onetap/?next=%2F",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"8.0.0\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "viewport-width": "954"
}


# get random proxy working
def get_proxies():
    proxy = None
    count = 1
    while True:
        print(colorama.Fore.BLUE + f"\r[{count}] đang lấy proxy..." + colorama.Style.RESET_ALL, end="")
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
            count += 1
            continue
    print()
    print(colorama.Fore.GREEN + f"[*] đã lấy được proxy -> {proxy}" + colorama.Style.RESET_ALL)
    return proxy

# encode password
def encrypt_password(password):
    timestamp = int(time.time())
    enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
    return enc_password



# login and get cookies instagram
def __login(username, password, proxy=None):
    global ERR, CSRF_TOKEN, COOKIE, headers

    # get proxy
    if proxy is True:
        proxy = {"http": get_proxies()}
    elif proxy is None:
        proxy = None
    elif isinstance(proxy, dict) and "http" in proxy or "https" in proxy:
        try:
            test_proxy = requests.get(url="https://google.com/",proxies=proxy,timeout=2)
            if test_proxy.status_code != 200:
                print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
                proxy = {"http": get_proxies()}
        except:
            print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
            proxy = {"http": get_proxies()}
    else:
        proxy = None

    session = requests.Session()
    url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"

    print(colorama.Fore.YELLOW + "[#] đang thay đổi user agent và lấy csrf token..." + colorama.Style.RESET_ALL)
    try:
        headers['User-Agent'] = random.choice(INSTAGRAM_USER_AGENT)
        headers['cookie'] = 'wd=954x746; dpr=1.25'
        r = requests.get("https://www.instagram.com/", headers=headers, proxies=proxy)
        CSRF_TOKEN = r.cookies['csrftoken']
        headers["X-CSRFToken"] = CSRF_TOKEN
        headers['cookie'] = "; ".join([f"{cookie.name}={cookie.value}" for cookie in r.cookies]) + '; wd=954x746; dpr=1.25'
    except Exception as e:
        print(e)
        return {"error": "có lỗi khi gửi yêu cầu để nhận csrf token"}
    
    # data have enc password
    data = {
        "username": username,
        "enc_password": encrypt_password(password),
        "queryParams": "{}",
        "optIntoOneTap": "false"
    }
    
    # send login requests to get cookies
    try:
        headers['method'] = "POST"
        response = session.post(url, data=data, headers=headers, proxies=proxy)
        cookies = session.cookies
        cookie_string = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
        cookie_string += "; ps_l=1; ps_n=1; wd=954x746"
    except:
        ERR = True
        return {"error": "có lỗi khi gửi yêu cầu đăng nhập"}
    
    # check response and return
    try:
        if response.status_code != 200:
            return {"error": "yêu cầu đăng nhập bị từ chối"}
        elif 'authenticated' not in response.json():
            return {"error": f"tài khoản {username} và mật khẩu (...) không tồn tại hoặc đã bị chặn!"}
        elif not response.json()['authenticated']:
            return {"error": f"tài khoản {username} và mật khẩu (...) không tồn tại hoặc đã bị chặn!"}
        elif response.json()['authenticated'] and response.json()['userId'] and response.json()['oneTapPrompt']:
            
            # pass captcha (if have)
            if captcha_dectect(cookie_string):
                p = PassInstagramCaptcha(cookie_str=cookie_string)
                o = p.captcha_auto_detecting_and_process()
                if "success" in o:
                    print(success_color(o['success']))
                else:
                    print(error_color(o['error']))
            else:
                print(system_color("Không phát hiện captcha!"))

            # skip verify automation
            print(colorama.Fore.BLUE + f"[#] đang bỏ qua xác thực tự động hóa..." + colorama.Style.RESET_ALL)
            res = pass_verify_automation(cookie_string)
            if "success" in res:
                print(colorama.Fore.GREEN + f"[*] {res['success']}" + colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.RED + f"[!] {res['error']}" + colorama.Style.RESET_ALL)

            return {"success": "đăng nhập thành công", "cookies": cookie_string, "proxy": proxy}
    except:
        ERR = True
        return {"error": f"có lỗi không xác định khi thực hiện đăng nhập tài khoản -> {username}"}


def login_instagram(username, password, proxy=None, instagram_cookies_path="instgaram_cookies.json"):
    # create empty cookies file (if it inexsist)
    if not os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "w") as file:
            json.dump({}, file)

    # load cookie file
    with open(instagram_cookies_path, 'r', encoding='utf-8') as file:
        cookies_data = json.load(file)
    
    # load exists proxy
    if proxy and proxy is not None and cookies_data['proxy'] is not None:
        if username in cookies_data and cookies_data[username]['proxy'] is not None:
            print(colorama.Fore.YELLOW + "[#] đã load proxy từ file" + colorama.Style.RESET_ALL)
            proxy = cookies_data[username]['proxy']

    if username in cookies_data:
        if cookies_data[username]['cookie'] == "" and ("username" in cookies_data[username] or "password" in cookies_data[username]):
            print(colorama.Fore.RED + f"[!] account {username} đã tồn tại, nhưng chưa có cookies" + colorama.Style.RESET_ALL)
            print(colorama.Fore.YELLOW + f"[*] tiến hành đăng nhập {username} để lấy phiên cookies..." + colorama.Style.RESET_ALL)
            login_output = __login(cookies_data[username]['username'], cookies_data[username]['password'], proxy)
            if 'success' in login_output:
                if "username" in cookies_data[username] and "password" in cookies_data[username]:
                    cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy'], "username": cookies_data[username]['username'], "password": cookies_data[username]['password']}
                else:
                    cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy']}
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_data, file)
            return login_output
        
        elif "username" in cookies_data[username] or "password" in cookies_data[username]:
            check_cookies_live = follow_instagram(
                username=username,
                insta_link="https://www.instagram.com/instagram",
                object_id="25025320",
                cookies=cookies_data[username]['cookie'],
                proxy=None
            )
            if 'following_status' in check_cookies_live:
                try:
                    test_proxy = requests.get(url="https://google.com/",proxies=proxy,timeout=2)
                    if test_proxy.status_code != 200:
                        print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
                        proxy = {"http": get_proxies()}
                        return {"success": "đã load cookies từ file", "cookies": cookies_data[username]['cookie'], "proxy": proxy}
                    else:
                        return {"success": "đã load cookies từ file", "cookies": cookies_data[username]['cookie'], "proxy": cookies_data[username]['proxy']}
                except:
                    print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
                    proxy = {"http": get_proxies()}
                    return {"success": "đã load cookies từ file", "cookies": cookies_data[username]['cookie'], "proxy": proxy}
            else:
                print(colorama.Fore.RED + "[#] cookies đã lưu đã bị lỗi! sẽ lấy cookies khác!" + colorama.Style.RESET_ALL)
                login_output = __login(cookies_data[username]['username'], cookies_data[username]['password'], proxy)
                if 'success' in login_output:
                    if "username" in cookies_data[username] and "password" in cookies_data[username]:
                        cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy'], "username": cookies_data[username]['username'], "password": cookies_data[username]['password']}
                    else:
                        cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy']}
                    with open(instagram_cookies_path, "w") as file:
                        json.dump(cookies_data, file)
                return login_output

    if username in cookies_data:
        check_cookies_live = follow_instagram(
            username=username,
            insta_link="https://www.instagram.com/instagram",
            object_id="25025320",
            cookies=cookies_data[username]['cookie'],
            proxy=None
        )
        if 'following_status' in check_cookies_live:
            try:
                test_proxy = requests.get(url="https://google.com/",proxies=proxy,timeout=2)
                if test_proxy.status_code != 200:
                    print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
                    proxy = {"http": get_proxies()}
                    return {"success": "đã load cookies từ file", "cookies": cookies_data[username]['cookie'], "proxy": proxy}
                else:
                    return {"success": "đã load cookies từ file", "cookies": cookies_data[username]['cookie'], "proxy": cookies_data[username]['proxy']}
            except:
                print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
                proxy = {"http": get_proxies()}
                return {"success": "đã load cookies từ file", "cookies": cookies_data[username]['cookie'], "proxy": proxy}
        else:
            print(colorama.Fore.RED + "[#] cookies đã lưu đã bị lỗi! sẽ lấy cookies khác!" + colorama.Style.RESET_ALL)
            login_output = __login(username, password, proxy)
            if 'success' in login_output:
                if "username" in cookies_data[username] and "password" in cookies_data[username]:
                    cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy'], "username": cookies_data[username]['username'], "password": cookies_data[username]['password']}
                else:
                    cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy']}
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_data, file)
            return login_output
    else:
        login_output = __login(username, password, proxy)
        if 'success' in login_output:
            if "username" in cookies_data[username] and "password" in cookies_data[username]:
                cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy'], "username": cookies_data[username]['username'], "password": cookies_data[username]['password']}
            else:
                cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy']}
            with open(instagram_cookies_path, "w") as file:
                json.dump(cookies_data, file)
        return login_output
