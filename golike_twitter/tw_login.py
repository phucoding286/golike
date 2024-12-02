import requests
import json
import colorama
import random
import os
from tw_interactions import tw_follow
colorama.init()

headers = {
  "authority": "api.twitter.com",
  "method": "POST",
  "path": "/1.1/onboarding/task.json?flow_name=login",
  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "vi",
  "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
  "content-length": "930",
  "content-type": "application/json",
  "cookie": "", # add later in code
  "origin": "https://twitter.com",
  "priority": "u=1, i",
  "referer": "https://twitter.com/",
  "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-site",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
  "x-client-transaction-id": "RzbFRPaMDR+IPONaBuOeMJBLIyUChfRxAC3w8MmgZ/IX31ItIbCThaQoReE/37eqLrKDgEX9BnRplJXkV+0/uCd3t+MNRA",
  "x-guest-token": "", # add later in code
  "x-twitter-active-user": "yes",
  "x-twitter-client-language": "vi"
}

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
user_agent = ua['UA']


# get random proxy working
def get_proxies():
    proxy = None
    while True:
        print(colorama.Fore.BLUE + f"đang lấy proxy cho login twitter..." + colorama.Style.RESET_ALL)
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


def __login(username, password, proxy: bool = True):
    global user_agent
    ua = random.choice(user_agent)
    headers['user-agent'] = ua

    # get proxy
    if proxy is True:
        proxies = {"http": get_proxies()}
    elif proxy is None or not proxy:
        proxies = None
    elif isinstance(proxy, dict) and "http" in proxy or "https" in proxy:
        try:
            test_proxy = requests.get(url="https://google.com/",proxies=proxy,timeout=2)
            if test_proxy.status_code != 200:
                print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
                proxies = {"http": get_proxies()}
        except:
            print(colorama.Fore.RED + "[#] proxy đã lưu đã bị lỗi! sẽ lấy proxy khác!" + colorama.Style.RESET_ALL)
            proxies = {"http": get_proxies()}
    else:
        proxies = None
    user_agent = { 'User-Agent' : ua }
    
    try:
        # lấy guest token
        r = requests.get("https://x.com/?mx=2", headers=user_agent, proxies=proxies)
        headers['x-guest-token'] = r.text.split("gt=")[1].split(';')[0]
        guest_id = f"""; guest_id={r.text.split('guestId":"')[1].split('"')[0]}"""
        guest_id_marketing = f"""; guest_id_marketing={r.text.split('"guest_id_marketing=')[1].split(";")[0]}"""
        guest_id_ads = f"""; guest_id_ads={r.text.split('"guest_id_ads=')[1].split(";")[0]}"""
        personalization_id = f"""; personalization_id={r.text.split('"personalization_id=')[1].split(";")[0]}"""
        gt = f"; gt={headers['x-guest-token']}"
        night_mode = "; night_mode=2"
        lang = "; lang=vi"

        url_flow_1 = "https://api.twitter.com/1.1/onboarding/task.json?flow_name=login"
        url_flow_2 = "https://api.twitter.com/1.1/onboarding/task.json"

        while True:
            try:
                # Flow 1
                data = {'' : ''}
                r = requests.post(url_flow_1, headers=headers, data=json.dumps(data), proxies=proxies)
                flow_token = json.loads(r.text)['flow_token']
                cookie = ';'.join(['%s=%s' % (name, value) for (name, value) in r.cookies.get_dict(domain=".twitter.com").items()])
                print(success_color(f"[*] flow_token 1: {flow_token}"))
                pass
            except:
                print(error_color("đã có lỗi khi lấy flow 1, sẽ thử lại"))
                continue

            # Flow 2
            data = {'flow_token' : flow_token, "subtask_inputs" : []}
            try:
                headers['cookie'] = cookie + guest_id + guest_id_ads + guest_id_marketing + personalization_id + gt + night_mode + lang
                r = requests.post(url_flow_2, headers=headers, json=data, proxies=proxies)
                flow_token = json.loads(r.text)['flow_token']
                print(success_color(f"[*] flow_token 2: {flow_token}"))
                pass
            except:
                print(error_color("đã có lỗi khi lấy flow 2, sẽ thử lại"))
                continue

            # Flow 3
            data = {"flow_token": flow_token ,"subtask_inputs":[{"subtask_id":"LoginEnterUserIdentifierSSO","settings_list":{"setting_responses":[{"key":"user_identifier","response_data":{"text_data":{"result":username}}}],"link":"next_link"}}]}
            try:
                r = requests.post(url_flow_2, headers=headers, json=data, proxies=proxies)
                if "errors" in r.json():
                    if r.json()['errors'][0]['message'] == "Rất tiếc, chúng tôi không thể tìm thấy tài khoản của bạn.":
                        return {"error": "username không tồn tại"}
                flow_token = json.loads(r.text)['flow_token']
                print(success_color(f"[*] flow_token 3: {flow_token}"))
                pass
            except:
                print(error_color("đã có lỗi khi lấy flow 3, sẽ thử lại"))
                continue

            # Flow 4
            data = {"flow_token": flow_token ,"subtask_inputs":[{"subtask_id":"LoginEnterPassword","enter_password":{"password":password,"link":"next_link"}}]}
            try:
                r = requests.post(url_flow_2, headers=headers, json=data, proxies=proxies)
                if "errors" in r.json():
                    if r.json()['errors'][0]['message'] == "Sai mật khẩu!":
                        return {"error": "sai mật khẩu"}
                flow_token = json.loads(r.text)['flow_token']
                print(success_color(f"[*] flow_token 4: {flow_token}"))
                break
            except:
                print(error_color("đã có lỗi khi lấy flow 4, sẽ thử lại"))
                continue

        if flow_token.split(":")[-1] == "8":
            return {"error": "account twitter này đã bị twitter chặn đăng nhập tạm thời"}
        
        # lấy cookie đã đăng nhập để tương tác sau này
        cookie = ';'.join(['%s=%s' % (name, value) for (name, value) in r.cookies.get_dict(domain=".twitter.com").items()])
        cookie += guest_id + guest_id_ads + guest_id_marketing + personalization_id + gt + night_mode + lang
        return {"success": "đã đăng nhập thành công", "cookies": cookie, "proxy": proxies}
    
    except Exception as e:
        return {"error": f"lỗi không xác định khi đăng nhập twitter, mã lỗi {e}"}
    

def login_twitter(username, password, proxy=None, twitter_cookies_path="twitter_cookies.json"):
    # create empty cookies file (if it inexsist)
    if not os.path.exists(twitter_cookies_path):
        with open(twitter_cookies_path, "w") as file:
            json.dump({}, file)

    # load cookie file
    with open(twitter_cookies_path, 'r', encoding='utf-8') as file:
        cookies_data = json.load(file)
    
    # load exists proxy
    if proxy and proxy is not None:
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
                with open(twitter_cookies_path, "w") as file:
                    json.dump(cookies_data, file)
            return login_output
    
        elif "username" in cookies_data[username] or "password" in cookies_data[username]:
            check_cookies_live = tw_follow(
                username=username,
                target_link="https://x.com/X",
                target_id="783214",
                cookie=cookies_data[username]['cookie'],
                proxy=None
            )
            if 'following' in check_cookies_live:
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
                    with open(twitter_cookies_path, "w") as file:
                        json.dump(cookies_data, file)
                return login_output
            
    if username in cookies_data:
        check_cookies_live = tw_follow(
            username=username,
            target_link="https://x.com/X",
            target_id="783214",
            cookie=cookies_data[username]['cookie'],
            proxy=None
        )
        if 'following' in check_cookies_live:
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
                with open(twitter_cookies_path, "w") as file:
                    json.dump(cookies_data, file)
            return login_output
    
    else:
        login_output = __login(username, password, proxy)
        if 'success' in login_output:
            if "username" in cookies_data[username] and "password" in cookies_data[username]:
                cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy'], "username": cookies_data[username]['username'], "password": cookies_data[username]['password']}
            else:
                cookies_data[username] = {'cookie': login_output['cookies'], "proxy": login_output['proxy']}
            with open(twitter_cookies_path, "w") as file:
                json.dump(cookies_data, file)
        return login_output