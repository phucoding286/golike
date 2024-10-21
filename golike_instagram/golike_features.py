import requests
import os
import json
from colorama import Fore, Style
import time
import colorama
import random
from login_instagram import login_instagram
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


# make waiting animation theme
def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(Fore.YELLOW + f"\r{i}s " + Style.RESET_ALL, end="")
        print(Fore.BLUE + text + Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0


# headers for golike account
GOLIKE_HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": "", # authorization golike (add later)
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=utf-8",
        "Host": "gateway.golike.net",
        "Origin": "https://app.golike.net",
        "Referer": "https://app.golike.net/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "t": "", # token golike (add later)
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)"
    }


# get job from golike
def get_jobs(instagram_golike_id):
    try:
        # requests for get job
        get_job = requests.get(
            url=f"https://gateway.golike.net/api/advertising/publishers/instagram/jobs?instagram_account_id={instagram_golike_id}&data=null",
            headers=GOLIKE_HEADERS
        )
        gjj = get_job.json()
        # if status code is 400 inference it's end jobs
        if gjj['status'] == 400:
            raise ValueError("đã hết jobs để làm")
        # else get needed data
        insta_link = gjj['data']['link']
        golike_user_id = gjj['data']['id']
        task_type = gjj['data']['type']
        object_id = gjj['data']['object_id']
        return insta_link, golike_user_id, task_type, object_id, {"status_code": gjj['status'], 'status': gjj['success']}
    except Exception as e:
        print(f"đã có lỗi khi nhận job mã lỗi: {e}")
        return {"error": True, "status_code": gjj['status']}



# drop job from golike when error
def drop_job(ads_id, object_id, account_id, task_type):
    try:
        response = requests.post(
            url="https://gateway.golike.net/api/advertising/publishers/instagram/skip-jobs",
            headers=GOLIKE_HEADERS,
            json={"account_id": account_id, "ads_id": ads_id, "object_id": object_id, "type": task_type}
        )
        if response.status_code == 200:
            return {"success": "đã bỏ job thành công"}
        else:
           return {"error": "đã có lỗi khi bỏ job"} 
    except:
        return {"error": "đã có lỗi khi bỏ job"}



# verify job on golike when complete task for get money
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
  


# check instagram accounts linking on golike
def check_instagram_account_id():
    response = requests.get(
        url="https://gateway.golike.net/api/instagram-account",
        headers=GOLIKE_HEADERS
    )
    resj = response.json()
    insta_id = [(insta_account_id['id'], insta_account_id['instagram_username']) for insta_account_id in resj['data']]
    return insta_id