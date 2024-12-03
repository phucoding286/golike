import requests, time

def pass_verify_automation(cookies):
    url = "https://www.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
    headers = {
        "Host": "www.instagram.com",
        "Cookie": "", # add later in code
        "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"",
        "X-Ig-Www-Claim": "hmac.AR191LHOjNv9hoWLKL5Bp6Jyofad9EuQg-vmTvE9RAQGZvjj",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua-Platform-Version": "",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Prefers-Color-Scheme": "dark",
        "X-Csrftoken": "", # add later in code
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "X-Ig-App-Id": "936619743392459",
        "Sec-Ch-Ua-Model": "",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Instagram-Ajax": "1017943380",
        "X-Bloks-Version-Id": "a2e134f798301e28e517956976df910b8fa9c85f9187c2963f77cdd733f46130",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
        "X-Asbd-Id": "129477",
        "Origin": "https://www.instagram.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.instagram.com/challenge/?next=https%3A%2F%2Fwww.instagram.com%2Faccounts%2Fonetap%2F%3Fnext%3D%252F%26__coig_challenged%3D1",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }
    data = {
        "challenge_context": "",
        "has_follow_up_screens": "false",
        "nest_data_manifest": "true"
    }
    headers['Cookie'] = cookies
    headers["X-Csrftoken"] = cookies.split("csrftoken=")[1].split(";")[0]
    try:
        response = requests.post(url, headers=headers, data=data)
        print(response.text)
        time.sleep(5)
        if "layout" in response.json():
            return {"success": "đã bỏ qua xác thực tự động hóa thành công"}
        else:
            return {"error": "đã có lỗi khi bỏ qua xác thực tự động hóa"}
    except:
        return {"error": "đã có lỗi không xác định khi bỏ qua xác thực tự động hóa"}
