import time
import requests

# encode password
def encrypt_password(password):
    timestamp = int(time.time())
    enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}"
    return enc_password

# login and get cookies instagram
def login_instagram(username, password):
    url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
    session = requests.Session()
    
    # get token CSRF
    csrf_token = session.get("https://www.instagram.com/").cookies['csrftoken']

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
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

    response = session.post(url, data=data, headers=headers)
    cookies = response.cookies
    cookie_string = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    if response.status_code != 200:
        return {"error": "yêu cầu đăng nhập bị từ chối"}
    elif not response.json()['authenticated']:
        return {"error": f"tài khoản {username} và mật khẩu (...) không tồn tại hoặc đã bị chặn!"}
    elif response.json()['authenticated'] and response.json()['userId'] and response.json()['oneTapPrompt']:
        return {"success": "đăng nhập thành công", "cookies": cookie_string}