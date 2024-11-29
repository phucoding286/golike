import requests, json, random, os, colorama, time
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
        print(colorama.Fore.YELLOW + f"\r[{i}s] " + colorama.Style.RESET_ALL, end="")
        print(colorama.Fore.BLUE + text + colorama.Style.RESET_ALL, end="")
        time.sleep(1)
    return 0

def goto_homepage_with_coig_challenged(cookie, ua_path="./ua.json"):
    with open(ua_path, "r") as file:
        ua = random.choice(json.load(file)['UA'])
    h = {
    "User-Agent": ua,
    "authority": "www.instagram.com",
    "method": "GET",
    "path": "/?__coig_challenged=1",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "vi",
    "cache-control": "max-age=0",
    "cookie": cookie,
    "dpr": "1.25",
    "priority": "u=0, i",
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
    r = requests.get(url="https://www.instagram.com/?__coig_challenged=1", headers=h)
    if r.status_code == 200:
        print(colorama.Fore.GREEN + f"[*] đã đến homepage với tham số coig_challenged thành công" + colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.RED + f"[!] đã đến homepage với tham số coig_challenged thất bại" + colorama.Style.RESET_ALL)


def inbox_request(username, cookies, ua_path="./ua.json", instagram_cookies_path="./instgaram_cookies.json"):
    with open(ua_path, "r") as file:
        ua = random.choice(json.load(file)['UA'])

    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']

    headers = {
        "authority": "www.instagram.com",
        "method": "POST",
        "path": "/api/v1/news/inbox/",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "content-length": "0",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": cookies,
        "origin": "https://www.instagram.com",
        "priority": "u=1, i",
        "referer": "https://www.instagram.com/direct/inbox/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-platform-version": "8.0.0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-asbd-id": "129477",
        "x-csrftoken": cookies.split("csrftoken=")[1].split(";")[0],
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR3crvgsPQsT-gdTESSsDhzefThSkbBNAobLs1-x-uRXOPBP",
        "x-instagram-ajax": "1017903014",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.post(
        url="https://www.instagram.com/api/v1/news/inbox/?__coig_challenged=1",
        headers=headers
    )
    try:
        r.json()
        
        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in r.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])
        
        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                cookies_load[username]['cookie'] = new_cookies_string
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)

        return {"status": "success", "cookies": new_cookies_string}
    except:
        return {"status": "fail"}
    

def pending_request(username, cookies, ua_path="./ua.json", instagram_cookies_path="./instgaram_cookies.json"):
    with open(ua_path, "r") as file:
        ua = random.choice(json.load(file)['UA'])

    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']
    
    headers = {
       "authority": "www.instagram.com",
        "method": "GET",
        "path": "/api/v1/friendships/pending/",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "cookie": cookies,
        "priority": "u=1, i",
        "referer": "https://www.instagram.com/direct/inbox/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-platform-version": "8.0.0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-asbd-id": "129477",
        "x-csrftoken": cookies.split("csrftoken=")[1].split(";")[0],
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR3crvgsPQsT-gdTESSsDhzefThSkbBNAobLs1-x-uRXOPBP",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.get(
        url="https://www.instagram.com/api/v1/friendships/pending/?__coig_challenged=1",
        headers=headers
    )
    try:
        r.json()

        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in r.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])

        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                cookies_load[username]['cookie'] = new_cookies_string
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)

        return {"status": "success", "cookies": new_cookies_string}
    except:
        return {"status": "fail"}
    

def follow_feed_request(username, cookies, ua_path="./ua.json", instagram_cookies_path="./instgaram_cookies.json"):
    with open(ua_path, "r") as file:
        ua = random.choice(json.load(file)['UA'])

    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']
    
    headers = {
        "authority": "www.instagram.com",
        "method": "GET",
        "path": "/api/v1/feed/reels_tray/?is_following_feed=false",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "cookie": cookies,
        "priority": "u=1, i",
        "referer": "https://www.instagram.com/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-platform-version": "8.0.0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-asbd-id": "129477",
        "x-csrftoken": cookies.split("csrftoken=")[1].split(";")[0],
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR3crvgsPQsT-gdTESSsDhzefThSkbBNAobLs1-x-uRXOPBP",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.get(
        url="https://www.instagram.com/api/v1/feed/reels_tray/?is_following_feed=false&__coig_challenged=1",
        headers=headers
    )
    try:
        r.json()
        
        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in r.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])

        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                cookies_load[username]['cookie'] = new_cookies_string
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)

        return {"status": "success", "cookies": new_cookies_string}
    except:
        return {"status": "fail"}


def ig_sso_user_request(username, cookies, ua_path="./ua.json", instagram_cookies_path="./instgaram_cookies.json"):
    with open(ua_path, "r") as file:
        ua = random.choice(json.load(file)['UA'])

    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']

    headers = {
        "authority": "www.instagram.com",
        "method": "POST",
        "path": "/api/v1/web/fxcal/ig_sso_users/",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "content-length": "0",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": cookies,
        "origin": "https://www.instagram.com",
        "priority": "u=1, i",
        "referer": "https://www.instagram.com/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-platform-version": "8.0.0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-asbd-id": "129477",
        "x-csrftoken": cookies.split("csrftoken=")[1].split(";")[0],
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR3crvgsPQsT-gdTESSsDhzefThSkbBNAobLs1-x-uRXOPBP",
        "x-instagram-ajax": "1017903757",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.post(
        url="https://www.instagram.com/api/v1/web/fxcal/ig_sso_users/?__coig_challenged=1",
        headers=headers
    )
    try:
        r.json()
        
        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in r.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])

        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                cookies_load[username]['cookie'] = new_cookies_string
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)

        return {"status": "success", "cookies": new_cookies_string}
    except:
        return {"status": "fail"}


def profile_request(username, cookies, ua_path="./ua.json", instagram_cookies_path="./instgaram_cookies.json"):
    with open(ua_path, "r") as file:
        ua = random.choice(json.load(file)['UA'])

    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']

    headers = {
        "authority": "www.instagram.com",
        "method": "GET",
        "path": f"/api/v1/web/get_profile_pic_props/{username}/",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "cookie": cookies,
        "priority": "u=1, i",
        "referer": "https://www.instagram.com/accounts/edit/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-platform-version": "8.0.0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-asbd-id": "129477",
        "x-csrftoken": cookies.split("csrftoken=")[1].split(";")[0],
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR3crvgsPQsT-gdTESSsDhzefThSkbBNAobLs1-x-uRXOPBP",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.get(
        url=f"https://www.instagram.com/api/v1/web/get_profile_pic_props/{username}/?__coig_challenged=1",
        headers=headers
    )
    try:
        r.json()
        
        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in r.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])

        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                cookies_load[username]['cookie'] = new_cookies_string
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)

        return {"status": "success", "cookies": new_cookies_string}
    except:
        return {"status": "fail"}


def account_edit_request(username, cookies, ua_path="./ua.json", instagram_cookies_path="./instgaram_cookies.json"):
    with open(ua_path, "r") as file:
        ua = random.choice(json.load(file)['UA'])

    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']

    headers = {
        "authority": "www.instagram.com",
        "method": "GET",
        "path": "/api/v1/accounts/edit/web_form_data/",
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "cookie": cookies,
        "priority": "u=1, i",
        "referer": "https://www.instagram.com/accounts/edit/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-platform-version": "8.0.0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-asbd-id": "129477",
        "x-csrftoken": cookies.split("csrftoken=")[1].split(";")[0],
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR3crvgsPQsT-gdTESSsDhzefThSkbBNAobLs1-x-uRXOPBP",
        "x-requested-with": "XMLHttpRequest"
    }
    r = requests.get(
        url=f"https://www.instagram.com/api/v1/accounts/edit/web_form_data/?__coig_challenged=1",
        headers=headers
    )
    try:
        r.json()
        
        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in r.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])

        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                cookies_load[username]['cookie'] = new_cookies_string
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)

        return {"status": "success", "cookies": new_cookies_string}
    except:
        return {"status": "fail"}
    

def send_random_fake_requests(username, cookies, sendtimes=5, fake_rqs_waitime=2, ua_path="./ua.json", instagram_cookies_path="./instgaram_cookies.json"):
    choose_list = ["inbox_request", "pending_request", "follow_feed_request", "ig_sso_user_request", "profile_request", "account_edit_request"]
    loop = False
    for i in range(sendtimes):
        i += 1
        random_choose = random.choice(choose_list)
        if random_choose == "inbox_request":
            output = inbox_request(username, cookies, ua_path, instagram_cookies_path)
            if output['status'] == 'success':
                print(success_color(f"\r[*] đã gửi yêu cầu giả 'inbox_request' thành công"), end="")
            else:
                print(error_color(f"\r[*] đã gửi yêu cầu giả 'inbox_request' không thành công"), end="")
        elif random_choose == "pending_request":
            output = pending_request(username, cookies, ua_path, instagram_cookies_path)
            if output['status'] == 'success':
                print(success_color(f"\r[*] đã gửi yêu cầu giả 'pending_request' thành công"), end="")
            else:
                print(error_color(f"\r[*] đã gửi yêu cầu giả 'pending_request' không thành công"), end="")
        elif random_choose == "follow_feed_request":
            output = follow_feed_request(username, cookies, ua_path, instagram_cookies_path)
            if output['status'] == 'success':
                print(success_color(f"\r[*] đã gửi yêu cầu giả 'follow_feed_request' thành công"), end="")
            else:
                print(error_color(f"\r[*] đã gửi yêu cầu giả 'follow_feed_request' không thành công"), end="")
        elif random_choose == "ig_sso_user_request":
            output = ig_sso_user_request(username, cookies, ua_path, instagram_cookies_path)
            if output['status'] == 'success':
                print(success_color(f"\r[*] đã gửi yêu cầu giả 'ig_sso_user_request' thành công"), end="")
            else:
                print(error_color(f"\r[*] đã gửi yêu cầu giả 'ig_sso_user_request' không thành công"), end="")
        elif random_choose == "profile_request":
            output = profile_request(username, cookies, ua_path, instagram_cookies_path)
            if output['status'] == 'success':
                print(success_color(f"\r[*] đã gửi yêu cầu giả 'profile_request' thành công"), end="")
            else:
                print(error_color(f"\r[*] đã gửi yêu cầu giả 'profile_request' không thành công"), end="")
        elif random_choose == "account_edit_request":
            output = account_edit_request(username, cookies, ua_path, instagram_cookies_path)
            if output['status'] == 'success':
                print(success_color(f"\r[*] đã gửi yêu cầu giả 'account_edit_request' thành công"), end="")
            else:
                print(error_color(f"\r[*] đã gửi yêu cầu giả 'account_edit_request' không thành công"), end="")
        waiting_ui(fake_rqs_waitime, f"[#] số lần -> {i}/{sendtimes}, vui lòng đợi {fake_rqs_waitime}s để tiếp tục gửi rqs mô phỏng...")
        loop = True
    if loop:
        print()