import requests
import colorama
import random
from pass_verify_automation import pass_verify_automation
import os, json, time
from fake_interaction import send_random_fake_requests, goto_homepage_with_coig_challenged
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

homepage_reqs_headers = {
    "authority": "www.instagram.com",
    "method": "GET",
    "path": "/tthan_h6/",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "dpr=1.25; mid=ZzGFrwALAAGi8jkPJNg8f_ev2qyK; datr=r4UxZ11SJYaAGhzS5h9IMJys; ig_did=3D8A971A-2FE9-4BD4-B1CD-2706FE6FBE91; ig_nrcb=1; ps_l=1; ps_n=1; ds_user_id=69747827988; sessionid=69747827988%3AHsCxZVBx9fZCVq%3A29%3AAYc9HG_7HZpWrow75t9ccJ-dViWprDsgrO8zwx92ZQ; csrftoken=ao3MZ0PgTY9jvlczPKfGPX8vdciAXBOu; rur=\"HIL,69747827988,1763620615:01f7c2f0752e187d99b3ce116786d15b3867a4494b9e9f238f60a8b47fcc19b51e5acfbe\"; wd=982x738",
    "dpr": "1.25",
    "priority": "u=0, i",
    "sec-ch-prefers-color-scheme": "dark",
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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "viewport-width": "981"
}

# instagram headers
INSTAGRAM_HEADER = {
    "authority": "www.instagram.com",
    "method": "POST",
    "path": "/graphql/query",
    "scheme": "https",
    "accept": "*/*",
    "accept-language": "us",
    "content-length": "1303",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "", # cookies instagram (add later)
    "origin": "https://www.instagram.com",
    "priority": "u=1, i",
    "referer": "",
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
    "user-agent": "",
    "x-asbd-id": "129477",
    "x-bloks-version-id": "d064162f4a1bc5cbc2a7ce44dd98b555613e0264ce1d0ebd6be60a79d3c58f44",
    "x-csrftoken": "", # csrftoken (add later)
    "x-fb-friendly-name": "PolarisAPIGetFrCookieQuery",
    "x-fb-lsd": "gtE021O5IF-2TGA5JwktM8",
    "x-ig-app-id": "936619743392459"
}
# instagram requests follow payloads
INSTAGRAM_FOLLOW_DATA = {
    "av": "17841469380937158",
  "__d": "www",
  "__user": "0",
  "__a": "1",
  "__req": "5",
  "__hs": "20040.HYP:instagram_web_pkg.2.1..0.1",
  "dpr": "1",
  "__ccg": "EXCELLENT",
  "__rev": "1018165176",
  "__s": "8ognoc:dtg3na:ur3c55",
  "__hsi": "7436812539460572753",
  "__dyn": "7xe5WwlEnwn8K2Wmm1twpUnwgU7S6EdF8aUco38w5ux60p-0LVE4W0qa0FE2awgo1EUhwGwQwoEcE2ygao1aU2iyo7u18wae4UaEW2G0AEco5G0zEnwhE0yK3qazo7u1xwIwbS1LwTwKG1pg2Xwr86C1mwrd6goK2O4UrAwCAxW1oCz8rwHwcOEy6U",
  "__csr": "l2IvlMH5On3tsGHJnW9lVV-KGiVVCAFpubAAARiiAQVFGHp9aVFaxdd5iARG5peFRy4jUK5kWKmnJoGExecF1l1mtejx51iEKuUgzoK5AHgZDCAx6rHD8FXyoymfyoSm13Bx7wgopyo01gNEy0UE0GN1OK0FU4a0ikg362O04co1RE0Elzoc83Nw2XA3HKlUdEpzGwBga4ve3a1qx20Xk2MEc-A1qqx52FYldg2ZBgS1eDgBEwbokzWc3C1Uwi8S48oxq0zo3twbF0aC1mw0uDE0k6w0GTw",
  "__comet_req": "7",
  "fb_dtsg": "NAcOB0Cchhvm1tgp03skndCs05s11HowtgeArT3Ac6z4nGAP7CEpPVg:17843729647189359:1731517833",
  "jazoest": "26213",
  "lsd": "t39uYtZ1La23AIGoUbu7qX",
  "__spin_r": "1018165176",
  "__spin_b": "trunk",
  "__spin_t": "1731517850",
  "fb_api_caller_class": "RelayModern",
  "fb_api_req_friendly_name": "PolarisStoriesV3AdsPoolQuery",
  "variables": "{\"target_user_id\":\"65635471598\",\"container_module\":\"profile\",\"nav_chain\":\"PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected\"}",
  "server_timestamps": "true",
  "doc_id": "7275591572570580"
}
# instagram requests like payloads
INSTAGRAM_LIKE_DATA = {
    "av": "17841469741829738",
    "__d": "www",
    "__user": "0",
    "__a": "1",
    "__req": "t",
    "__hs": "20019.HYP:instagram_web_pkg.2.1..0.1",
    "dpr": "1",
    "__ccg": "EXCELLENT",
    "__rev": "1017590237",
    "__s": "spxbsq:cbnr63:a7dtyg",
    "__hsi": "7428978248364380201",
    "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o1DU2_CwjE1xoswaq0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo31w9O1TwQzXwae4UaEW2G0AEco5G0zK5o4q3y1Sx-0lKq2-azqwt8d-2u2J0bS1LwTwKG1pg2fwxyo6O1FwlEcUed6goK2O4UrAwHxW1oCz8rDwzwrE5SEymUhw",
    "__csr": "igJ0AijgX5HLFPiRblOikpF9l9kPn8luh4ALl4R8zz99kiEC8ACGQUzQWXxeiKHKbiIGGiih95BjGHh8Gm9DCQEF2F4jKcx3CxGm9-9K9wIjy8ySiqEjmGKmHoLAKXLAKcCBjCCy9UC58y2CWg01eeu19CDwhQHF0Awda0pKuE1Po11oq8VQaIw6xwzwTAg3Kw16204sUyhw28U7q1388zuK619QQnigrwmo1yiyE-3W3QFUAwR5KR282DDwGooxUg9yEdUay1K7C1qGdw_zVEO0NXAwlU3BwM2y20jwaK6A5U0c4E04GC06Zo",
    "__comet_req": "7",
    "fb_dtsg": "NAcOD8Fa84LbWEWYvLE6tdA0uxBP20oA7QRYtgNlWFx9ojdVcT1XzMQ:17865379441060568:1729692751",
    "jazoest": "26119",
    "lsd": "1BJCA8gh8AoA_mi8ju3VAA",
    "__spin_r": "1017590237",
    "__spin_b": "trunk",
    "__spin_t": "1729693787",
    "fb_api_caller_class": "RelayModern",
    "fb_api_req_friendly_name": "usePolarisLikeMediaLikeMutation",
    "variables": ('{'f'"media_id":"test","container_module":null,"inventory_source":null,"ranking_info_token":null,"nav_chain":null''}'),
    "server_timestamps": "true",
    "doc_id": "8552604541488484"
}
#
TEST_PAYLOAD = {
  "av": "17841469380937158",
  "__d": "www",
  "__user": "0",
  "__a": "1",
  "__req": "5",
  "__hs": "20040.HYP:instagram_web_pkg.2.1..0.1",
  "dpr": "1",
  "__ccg": "EXCELLENT",
  "__rev": "1018165176",
  "__s": "8ognoc:dtg3na:ur3c55",
  "__hsi": "7436812539460572753",
  "__dyn": "7xe5WwlEnwn8K2Wmm1twpUnwgU7S6EdF8aUco38w5ux60p-0LVE4W0qa0FE2awgo1EUhwGwQwoEcE2ygao1aU2iyo7u18wae4UaEW2G0AEco5G0zEnwhE0yK3qazo7u1xwIwbS1LwTwKG1pg2Xwr86C1mwrd6goK2O4UrAwCAxW1oCz8rwHwcOEy6U",
  "__csr": "l2IvlMH5On3tsGHJnW9lVV-KGiVVCAFpubAAARiiAQVFGHp9aVFaxdd5iARG5peFRy4jUK5kWKmnJoGExecF1l1mtejx51iEKuUgzoK5AHgZDCAx6rHD8FXyoymfyoSm13Bx7wgopyo01gNEy0UE0GN1OK0FU4a0ikg362O04co1RE0Elzoc83Nw2XA3HKlUdEpzGwBga4ve3a1qx20Xk2MEc-A1qqx52FYldg2ZBgS1eDgBEwbokzWc3C1Uwi8S48oxq0zo3twbF0aC1mw0uDE0k6w0GTw",
  "__comet_req": "7",
  "fb_dtsg": "NAcOB0Cchhvm1tgp03skndCs05s11HowtgeArT3Ac6z4nGAP7CEpPVg:17843729647189359:1731517833",
  "jazoest": "26213",
  "lsd": "t39uYtZ1La23AIGoUbu7qX",
  "__spin_r": "1018165176",
  "__spin_b": "trunk",
  "__spin_t": "1731517850",
  "fb_api_caller_class": "RelayModern",
  "fb_api_req_friendly_name": "PolarisStoriesV3AdsPoolQuery",
  "variables": "",
  "server_timestamps": "true",
  "__coig_challenged": "1",
  "doc_id": ""
}

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



# like instagram target
def like_instagram(username, insta_link, object_id, cookies: str, proxy: bool = True, instagram_cookies_path="instgaram_cookies.json"):
    global INSTAGRAM_LIKE_DATA, TEST_PAYLOAD
    global INSTAGRAM_HEADER
    TEST_PAYLOAD['doc_id'] = INSTAGRAM_LIKE_DATA['doc_id']
    
    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load and proxy:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']

    # get x-csrftoken from string cookies and add it in headers
    INSTAGRAM_HEADER["x-csrftoken"] = cookies.split("csrftoken=")[1].split(";")[0]
    INSTAGRAM_HEADER['cookie'] = cookies # add cookies in headers
    INSTAGRAM_HEADER['referer'] = insta_link # add target instagram link on headers
    INSTAGRAM_HEADER['user-agent'] = random.choice(INSTAGRAM_USER_AGENT) # add random user agent in headers
    TEST_PAYLOAD["variables"] = ('{'f'"media_id":"{object_id}","container_module":null,"inventory_source":null,"ranking_info_token":null,"nav_chain":null''}')
    
    goto_homepage_with_coig_challenged(cookies)
    homepage_reqs_headers['path'] = f"/{insta_link.split('/')[-1]}/"
    print(wait_color("[#] đang đi đến trang mục tiêu trước khi tương tác"))
    try:
        r = requests.get(insta_link+"/?__coig_challenged=1", headers=homepage_reqs_headers)
        if r.status_code == 200:
            print(success_color("[*] đã đến trang mục tiêu thành công"))
        else:
            print(error_color("[!] đã đến trang mục tiêu thất bại"))
    except:
        print(error_color("[!] đã đến trang mục tiêu thất bại"))

    # get proxy
    if proxy is True:
        proxy = {"http": get_proxies()}
    elif proxy is None:
        proxy = None
    elif isinstance(proxy, dict) and "http" in proxy or "https" in proxy:
        pass
    else:
        proxy = None
        
    try:
        response = requests.post(
            url="https://www.instagram.com/graphql/query/?__coig_challenged=1",
            headers=INSTAGRAM_HEADER,
            data=TEST_PAYLOAD,
            proxies=proxy
        )
        
        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in response.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])
        
        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                if proxy:
                    if "username" in cookies_load[username] or "password" in cookies_load[username]:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": proxy, "password": cookies_load[username]['password'], "username": cookies_load[username]["username"]}
                    else:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": proxy}
                else:
                    if "username" in cookies_load[username] or "password" in cookies_load[username]:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": None, "password": cookies_load[username]['password'], "username": cookies_load[username]["username"]}
                    else:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": None}
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)

        # result
        insta_json_res = response.json()
        if "errors" in insta_json_res:
            return {'error': "lỗi khi like"}
        insta_json_res['extensions']['cookies'] = new_cookies_string
        return insta_json_res['extensions']
    
    # can inference None type error is this target is not found
    except TypeError as e:
        print(error_color(f"lỗi like instagram -> {e}"))
        return {"page_not_found": "trang instagram này không tồn tại!", 'error': "lỗi khi like"}
    # unknow error
    except Exception as e:
        print(error_color(f"lỗi like instagram -> {e}"))
        return {'error': "lỗi khi like"}



# following instagram target
def follow_instagram(username, insta_link, object_id, cookies: str, proxy: bool = True, instagram_cookies_path="instgaram_cookies.json", debug=False):
    global INSTAGRAM_FOLLOW_DATA, TEST_PAYLOAD
    global INSTAGRAM_HEADER
    TEST_PAYLOAD['doc_id'] = INSTAGRAM_FOLLOW_DATA['doc_id']

    # load old cookies storaged in file
    if os.path.exists(instagram_cookies_path):
        with open(instagram_cookies_path, "r") as file:
            cookies_load = json.load(file)
        if username in cookies_load and proxy:
            if cookies_load[username]['cookie'] != "":
                cookies = cookies_load[username]['cookie']

    # get x-csrftoken from string cookies and add it in headers
    INSTAGRAM_HEADER["x-csrftoken"] = cookies.split("csrftoken=")[1].split(";")[0]
    INSTAGRAM_HEADER['cookie'] = cookies # add cookies in headers
    INSTAGRAM_HEADER['referer'] = insta_link # add target instagram link on headers
    INSTAGRAM_HEADER['user-agent'] = random.choice(INSTAGRAM_USER_AGENT) # add random user agent in headers
    TEST_PAYLOAD["variables"] = ('{'f'"target_user_id": "{object_id}",''"container_module": "profile",''"nav_chain": "PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected"''}')

    goto_homepage_with_coig_challenged(cookies)
    homepage_reqs_headers['user-agent'] = random.choice(INSTAGRAM_USER_AGENT)
    homepage_reqs_headers['path'] = f"/{insta_link.split('/')[-1]}/"
    print(wait_color("[#] đang đi đến trang mục tiêu trước khi tương tác"))
    try:
        r = requests.get(insta_link+"/?__coig_challenged=1", headers=homepage_reqs_headers)
        if r.status_code == 200:
            print(success_color("[*] đã đến trang mục tiêu thành công"))
        else:
            print(error_color("[!] đã đến trang mục tiêu thất bại"))
    except:
        print(error_color("[!] đã đến trang mục tiêu thất bại"))

    # get proxy
    if proxy is True:
        proxy = {"http": get_proxies()}
    elif proxy is None:
        proxy = None
    elif isinstance(proxy, dict) and "http" in proxy or "https" in proxy:
        pass
    else:
        proxy = None
        
    try:
        response = requests.post(
            url="https://www.instagram.com/graphql/query/?__coig_challenged=1",
            headers=INSTAGRAM_HEADER,
            data=TEST_PAYLOAD,
            proxies=proxy
        )

        if debug:
            print(response.text)
        
        # create new cookies
        current_cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies.split("; ")}
        for cookie_key, cookie_value in response.cookies.get_dict().items():
            current_cookies_dict[cookie_key] = cookie_value
        new_cookies_string = "; ".join([f"{key}={value}" for key, value in current_cookies_dict.items()])

        # save new cookie in storage cookie file
        if os.path.exists(instagram_cookies_path):
            with open(instagram_cookies_path, "r") as file:
                cookies_load = json.load(file)
            if username in cookies_load:
                if proxy:
                    if "username" in cookies_load[username] or "password" in cookies_load[username]:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": proxy, "password": cookies_load[username]['password'], "username": cookies_load[username]["username"]}
                    else:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": proxy}
                else:
                    if "username" in cookies_load[username] or "password" in cookies_load[username]:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": None, "password": cookies_load[username]['password'], "username": cookies_load[username]["username"]}
                    else:
                        cookies_load[username] = {"cookie": new_cookies_string, "proxy": None}
                with open(instagram_cookies_path, "w") as file:
                    json.dump(cookies_load, file)
        
        insta_json_res = response.json()['data']["xdt_create_friendship"]["friendship_status"]
        return {"following_status": insta_json_res["following"], "outgoing_request": insta_json_res['outgoing_request'], 'cookies': new_cookies_string}
    
    # can inference None type error is this target is not found
    except TypeError as e:
        print(error_color(f"lỗi follow instagram -> {e}"))
        return {"page_not_found": "trang instagram này không tồn tại!", 'error': "lỗi khi follow"}
    # unknow error
    except Exception as e:
        print(error_color(f"lỗi follow instagram -> {e}"))
        return {'error': "lỗi khi follow"}