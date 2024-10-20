import requests
import os
import json
from colorama import Fore, Style
import time
import colorama
import random
from login_instagram import login_instagram
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

GOLIKE_HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3Mjc5Mjk1OTYsImV4cCI6MTc1OTQ2NTU5NiwibmJmIjoxNzI3OTI5NTk2LCJqdGkiOiIwODVJVXBmUnNjT1Fqb1RFIiwic3ViIjoyODc2NDY2LCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.w1xDhJcTqcXU8t5BrIs6HH-GIOP4U5Oj3-BY1SmGJLU",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=utf-8",
        "Host": "gateway.golike.net",
        "Origin": "https://app.golike.net",
        "Referer": "https://app.golike.net/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "t": "VFZSamVVNTZhM3BPZW1NeFQxRTlQUT09",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)"
    }

def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(Fore.YELLOW + f"\r{i}s " + Style.RESET_ALL, end="")
        print(Fore.BLUE + text + Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0

def get_jobs(instagram_golike_id):
    try:
        get_job = requests.get(
            url=f"https://gateway.golike.net/api/advertising/publishers/instagram/jobs?instagram_account_id={instagram_golike_id}&data=null",
            headers=GOLIKE_HEADERS
        )
        gjj = get_job.json()
        if gjj['status'] == 400:
            raise ValueError("đã hết jobs để làm")
        insta_link = gjj['data']['link']
        golike_user_id = gjj['data']['id']
        task_type = gjj['data']['type']
        object_id = gjj['data']['object_id']
        return insta_link, golike_user_id, task_type, object_id, {"status_code": gjj['status'], 'status': gjj['success']}
    except Exception as e:
        print(f"đã có lỗi khi nhận job mã lỗi: {e}")
        return {"error": True, "status_code": gjj['status']}
    
def drop_job(ads_id, object_id, account_id):
    try:
        response = requests.post(
            url="https://gateway.golike.net/api/advertising/publishers/instagram/skip-jobs",
            headers=GOLIKE_HEADERS,
            json={"account_id": account_id, "ads_id": ads_id, "object_id": object_id, "type": "follow"}
        )
        if response.status_code == 200:
            return {"success": "đã bỏ job thành công"}
        else:
           return {"error": "đã có lỗi khi bỏ job"} 
    except:
        return {"error": "đã có lỗi khi bỏ job"}


def verify_complete_job(ads_id, account_id):
  try:
      complete_job = requests.post(
        url="https://gateway.golike.net/api/advertising/publishers/instagram/complete-jobs",
        headers=GOLIKE_HEADERS,
        json={"async": True, "captcha": "recaptcha", "data": None, "instagram_account_id": account_id, "instagram_users_advertising_id": ads_id}
      )
      c = complete_job.json()
      return (c['status'], f"trạng thái: [{c['status']}] -> {'thành công' if c['success'] else 'không thành công'}", f"tiền công -> {c['data']['prices']}đ")
  except Exception as e:
      print(f"đã có lỗi khi xác minh hoàn thành job mã lỗi: {e}")
      return {"error": True}
  

def check_instagram_account_id():
    response = requests.get(
        url="https://gateway.golike.net/api/instagram-account",
        headers=GOLIKE_HEADERS
    )
    resj = response.json()
    insta_id = [(insta_account_id['id'], insta_account_id['instagram_username']) for insta_account_id in resj['data']]
    return insta_id



INSTAGRAM_HEADER = {
        "authority": "www.instagram.com",
        "method": "POST",
        "path": "/graphql/query",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "us",
        "content-length": "1303",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "dpr=1.25; ig_nrcb=1; mid=ZwKWggALAAEDrWL7H8N2TSSwzwA9; ig_did=40FB9C01-DC10-49FA-8CC8-156893EB5825; datr=lZYCZxR6Id0TJUE0KwqHC8-p; ds_user_id=65444176476; sessionid=65444176476%3AfJ2yFeRc7q4bDy%3A6%3AAYfjd4HuNL7B82ukA2gfhTaVnup-W5aFlZVca7FjlQ; csrftoken=ep2QzalKQUaJFJm2Kp80gc1xtmdeJyNe; shbid=\"17201\\05465444176476\\0541759759058:01f70e33f8d7daee4e0a336add6591854f7d340ba878a5d71c76b544fd22acd10168d739\"; shbts=\"1728223058\\05465444176476\\0541759759058:01f72eb726945e659cb78b5c01c785bcee35b279615be7f41ba90d13d1c27de0d7bbda15\"; wd=822x746; rur=\"CCO\\05465444176476\\0541759759576:01f762a4308eebbf945a0e9d8b84f0c83a9e8693e93dfef225f653da67d8bb5c00231ef8\"",
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
        "x-csrftoken": "ep2QzalKQUaJFJm2Kp80gc1xtmdeJyNe",
        "x-fb-friendly-name": "PolarisAPIGetFrCookieQuery",
        "x-fb-lsd": "gtE021O5IF-2TGA5JwktM8",
        "x-ig-app-id": "936619743392459"
    }
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
INSTAGRAM_USER_AGENT = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0."
    ]


def get_proxies():
    proxy = None
    count = 1
    while True:
        print(colorama.Fore.BLUE + f"\r{count} đang lấy proxy cho instagram..." + colorama.Style.RESET_ALL, end="")
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
    print()
    print(colorama.Fore.GREEN + f"đã lấy proxy {proxy} thành công!" + colorama.Style.RESET_ALL)
    return proxy


def follow_instagram(insta_link, object_id, cookies: str):
    global INSTAGRAM_DATA
    global INSTAGRAM_HEADER
    INSTAGRAM_HEADER["x-csrftoken"] = cookies.split("csrftoken=")[1].split(";")[0]
    INSTAGRAM_HEADER['cookie'] = cookies
    INSTAGRAM_HEADER['referer'] = insta_link
    INSTAGRAM_HEADER['user-agent'] = random.choice(INSTAGRAM_USER_AGENT)
    INSTAGRAM_DATA["variables"] = ('{'f'"target_user_id": "{object_id}",''"container_module": "profile",''"nav_chain": "PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected"''}')
    print(wait_color("đang thực hiện kiểm tra tài khoản instagram mục tiêu..."))
    try:
        response = requests.post(
            url="https://www.instagram.com/graphql/query",
            headers=INSTAGRAM_HEADER,
            data=INSTAGRAM_DATA,
            proxies={'http': get_proxies()}
        )
        insta_json_res = response.json()['data']["xdt_create_friendship"]["friendship_status"]
        return {"following_status": insta_json_res["following"], "outgoing_request": insta_json_res['outgoing_request']}
    except TypeError as e:
        print(f"lỗi follow instagram: {e}")
        return {"page_not_found": "trang instagram này không tồn tại!"}
    except Exception as e:
        print(f"lỗi follow instagram: {e}")
        return {'error': True}
    

def golike_instagram_auto(instagram_golike_id_input, cookies_inp, wait_time, current_account):
    while True:
        print(system_color(f"account đang làm việc hiện tại là: {current_account}"))
        r_get_jobs = get_jobs(instagram_golike_id_input)
        if "error" in r_get_jobs:
            return {"error": r_get_jobs['error']}
        if r_get_jobs[2] != "follow":
            print(error_color("không phải nhiệm vụ follow"))
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input)))
            waiting_ui(1, "vui lòng chờ đợi 1 giây")
            continue
        
        print(purple_color(f"mục tiêu: {r_get_jobs[0]}"))
        follow_output = follow_instagram(r_get_jobs[0], r_get_jobs[3], cookies=cookies_inp)
        print(purple_color(follow_output))
        
        if 'following_status' in follow_output:
            if not follow_output['following_status'] and not follow_output['outgoing_request']:
                print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input)))
                return {"error": "account instagram này đã bị chặn follow, vui lòng đổi tài khoản mới"}
        elif "page_not_found" in follow_output:
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input)))
            waiting_ui(wait_time, f"vui lòng chờ đợi {wait_time}s")
            continue
        elif "error" in follow_output:
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input)))
            return {"error": "account bị chặn hoặc lỗi không xác định"}

        waiting_ui(10, "vui lòng chờ đợi 10s để xác minh job")
        output = verify_complete_job(r_get_jobs[1], instagram_golike_id_input)
        if "error" in output:
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input)))
            waiting_ui(wait_time, f"vui lòng chờ đợi {wait_time}s")
            continue
        else:
            print(success_color(output))
            waiting_ui(wait_time, f"vui lòng chờ đợi {wait_time}s")
            continue


def golike_instagram_ui():
    global GOLIKE_HEADERS

    golike_authorization_input = input(system_color("nhập authorization golike của bạn\n>>> "))
    GOLIKE_HEADERS['Authorization'] = golike_authorization_input
    golike_token_input = input(system_color("nhập token golike của bạn\n>>> "))
    GOLIKE_HEADERS['t'] = golike_token_input
    PASSWORDS = json.load(open("./golike_instagram/password.json"))
    PASSWORDS = PASSWORDS['passwords']
    
    print(system_color("các id của bạn là:"))
    count = 1
    IDs = []
    nicknames = []
    for nickname_id in check_instagram_account_id():
        print(success_color(f"{count}. id: {nickname_id[0]} instagram_username: {nickname_id[1]}"))
        count += 1
        IDs.append(nickname_id[0])
        nicknames.append(nickname_id[1])

    wait_time = int(input(system_color("Nhập số thời gian chờ trước khi follow tiếp theo\n>>> ")))

    while True:
        sum_login_error = 0
        sum_activate_error = 0
        for i in range(len(IDs)):
            cookies = None
            for passwd in PASSWORDS:
                login_output = login_instagram(nicknames[i], passwd)
                if "error" in login_output:
                    print(error_color(login_output['error']))
                    waiting_ui(timeout=5, text="đợi 5s để tiếp tục")
                    continue
                else:
                    sum_login_error = 0
                    print(success_color(login_output['success']))
                    cookies = login_output['cookies']
            if cookies is None:
                if sum_login_error >= len(IDs):
                    waiting_ui(timeout=1200, text="vui lòng đợi 10 phút để check lại và chạy follow cho tất cả tài khoản")
                    sum_login_error = 0
                else:
                    sum_login_error += 1
                    waiting_ui(5, "đợi 5s để tiếp tục")
                continue
            else:
                golike_auto_output = golike_instagram_auto(IDs[i], cookies, wait_time, nicknames[i])
                if "error" in golike_auto_output:
                    sum_activate_error += 1
                    print(error_color(golike_auto_output['error']))
                    if sum_activate_error > len(IDs):
                        waiting_ui(timeout=1200, text="vui lòng đợi 10p (1200s) để check lại và chạy follow cho tất cả tài khoản")
                else:
                    sum_activate_error = 0


def add_passwords_ui():
    while True:
        try:
            passwd_inp = input(system_color("nhập thêm password instagram của bạn\n>>> "))
            if os.path.exists("./golike_instagram/password.json"):
                passwords = json.load(open("./golike_instagram/password.json", "r"))
                passwords['passwords'].append(passwd_inp)
            else:
                passwords = {"passwords": [passwd_inp]}
            json.dump(passwords, open("./golike_instagram/password.json", 'w'))
            print(success_color("đã thêm password thành công"))
        except Exception as e:
            print(e)
            print(error_color("đã có lỗi khi thêm password"))


if __name__ == "__main__":
    while True:
        choose_table = [(print(system_color("1. chạy tool golike instagram")), 0), (print(system_color("2. thêm password instagram")), 1)]
        try:
            choose_inp = int(input(system_color("nhập lựa chọn của bạn\n>>> ")))
            choose_table = choose_table[choose_inp-1][-1]
        except:
            print(error_color("vui lòng nhập đúng số thứ tự"))
        if choose_table == 0:
            golike_instagram_ui()
        else:
            add_passwords_ui()