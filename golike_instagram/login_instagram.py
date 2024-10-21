import time
import requests
import colorama
import random
colorama.init()


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
        print(colorama.Fore.BLUE + f"đang lấy proxy cho login instagram..." + colorama.Style.RESET_ALL)
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

# encode password
def encrypt_password(password):
    timestamp = int(time.time())
    enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
    return enc_password

# login and get cookies instagram
def login_instagram(username, password):
    url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
    session = requests.Session()
    # lấy proxy cho login instagram
    proxies = {'http': get_proxies()}
    
    # get token CSRF
    csrf_token = session.get("https://www.instagram.com/", proxies=proxies).cookies['csrftoken']

    headers = {
        "User-Agent": random.choice(INSTAGRAM_USER_AGENT),
        "X-CSRFToken": csrf_token,
        "X-Instagram-Ajax": "1",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*"
    }

    data = {
        "username": username,
        "enc_password": encrypt_password(password),
        "queryParams": "{}",
        "optIntoOneTap": "false"
    }

    response = session.post(url, data=data, headers=headers, proxies=proxies)
    cookies = response.cookies
    cookie_string = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    if response.status_code != 200:
        return {"error": "yêu cầu đăng nhập bị từ chối"}
    elif not response.json()['authenticated']:
        return {"error": f"tài khoản {username} và mật khẩu (...) không tồn tại hoặc đã bị chặn!"}
    elif response.json()['authenticated'] and response.json()['userId'] and response.json()['oneTapPrompt']:
        return {"success": "đăng nhập thành công", "cookies": cookie_string}