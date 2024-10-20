import requests
import os
from colorama import Fore, Style
import time
import colorama
colorama.init()

def error_color(string: str):
    return colorama.Fore.RED + str(string) + colorama.Style.RESET_ALL
def success_color(string: str):
    return colorama.Fore.GREEN + str(string) + colorama.Style.RESET_ALL
def system_color(string: str):
    return colorama.Fore.YELLOW + str(string) + colorama.Style.RESET_ALL
def wait_color(string: str):
    return colorama.Fore.BLUE + str(string) + colorama.Style.RESET_ALL

HEADERS = {
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

def get_jobs(tiktok_golike_id):
    try:
        get_job = requests.get(
            url=f"https://gateway.golike.net/api/advertising/publishers/tiktok/jobs?account_id={tiktok_golike_id}&data=null",
            headers=HEADERS
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
            url="https://gateway.golike.net/api/advertising/publishers/tiktok/skip-jobs",
            headers=HEADERS,
            json={"account_id": account_id, "ads_id": ads_id, "object_id": object_id, "type": "follow"}
        )
        print(response.text)
        if response.status_code == 200:
            return {"success": "đã bỏ job thành công"}
        else:
           return {"error": "đã có lỗi khi bỏ job"} 
    except:
        return {"error": "đã có lỗi khi bỏ job"}


def verify_complete_job(ads_id, account_id):
  try:
      complete_job = requests.post(
        url="https://gateway.golike.net/api/advertising/publishers/tiktok/complete-jobs",
        headers=HEADERS,
        json={"async": True, "ads_id": ads_id, "data": None, "account_id": account_id}
      )
      c = complete_job.json()
      return (c['status'], f"trạng thái: [{c['status']}] -> {'thành công' if c['success'] else 'không thành công'}", f"tiền công -> {c['data']['prices']}đ")
  except Exception as e:
      print(f"đã có lỗi khi xác minh hoàn thành job mã lỗi: {e}")
      return {"error": True}
  
def check_instagram_account_id():
    response = requests.get(
        url="https://gateway.golike.net/api/tiktok-account",
        headers=HEADERS
    )
    resj = response.json()
    insta_id = [(insta_account_id['id'], insta_account_id['nickname']) for insta_account_id in resj['data']]
    return insta_id
  
if __name__ == "__main__":
    print("các id của bạn là:")
    count = 1
    IDs = []
    for nickname_id in check_instagram_account_id():
        print(f"{count}. id: {nickname_id[0]} nickname: {nickname_id[1]}")
        count += 1
        IDs.append(nickname_id[0])
    tiktok_golike_id_input = IDs[int(input("vui lòng nhập vào số thứ tự tương ứng account id của bạn: "))-1]
    while True:
        r_get_jobs = get_jobs(tiktok_golike_id_input)
        if "error" in r_get_jobs:
            waiting_ui(5, "vui lòng chờ đợi 5 giây")
            continue
        if r_get_jobs[2] != "follow":
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], tiktok_golike_id_input)))
            waiting_ui(1, "vui lòng chờ đợi 1 giây")
            continue
        os.system(f"termux-open-url {r_get_jobs[0]}")
        waiting_ui(5, "vui lòng chờ đợi 5 giây")
        output = verify_complete_job(r_get_jobs[1], tiktok_golike_id_input)
        if "error" in output:
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], tiktok_golike_id_input)))
        else:
            print(success_color(output))
            continue