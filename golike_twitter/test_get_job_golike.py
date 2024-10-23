import requests

# headers for golike account
GOLIKE_HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9nYXRld2F5LmdvbGlrZS5uZXRcL2FwaVwvbG9naW4iLCJpYXQiOjE3Mjg3MTI0OTMsImV4cCI6MTc2MDI0ODQ5MywibmJmIjoxNzI4NzEyNDkzLCJqdGkiOiJ5MVZDTVZoTkQzdzNuMnhVIiwic3ViIjoyODc2NDY2LCJwcnYiOiJiOTEyNzk5NzhmMTFhYTdiYzU2NzA0ODdmZmYwMWUyMjgyNTNmZTQ4In0.M6E40rosApqFQjs8NLfo8M_3kTcQpaLW2STaliMyLwI", # authorization golike (add later)
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

# check twitter accounts linking on golike
def check_tw_account_id():
    response = requests.get(
        url="https://gateway.golike.net/api/twitter-account",
        headers=GOLIKE_HEADERS
    )
    resj = response.json()
    tw_id = [(tw_account_id['id'], tw_account_id['screen_name']) for tw_account_id in resj['data']]
    return tw_id


# get job from golike
def get_jobs(tw_golike_id):
    try:
        # requests for get job
        get_job = requests.get(
            url=f"https://gateway.golike.net/api/advertising/publishers/twitter/jobs?account_id={tw_golike_id}",
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
def drop_job(ads_id, object_id, account_id):
    try:
        response = requests.post(
            url="https://gateway.golike.net/api/advertising/publishers/twitter/skip-jobs",
            headers=GOLIKE_HEADERS,
            json={"account_id": account_id, "ads_id": ads_id, "object_id": object_id}
        )
        if response.status_code == 200:
            return {"success": "đã bỏ job thành công"}
        else:
           return {"error": "đã có lỗi khi bỏ job"} 
    except:
        return {"error": "đã có lỗi khi bỏ job"}

account_id, username = check_tw_account_id()[0]
r_get_job = get_jobs(account_id)
print(r_get_job)
print(drop_job(r_get_job[1], r_get_job[3], account_id))