import requests
import json
import colorama
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


def login_twitter(username, password, proxy: bool = True):
    if proxy:
        proxies = {"http": get_proxies()}
    else:
        proxies = None
    user_agent = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
    
    try:
        # lấy guest token
        r = requests.get("https://x.com/?mx=2", headers=user_agent, proxies=proxies)
        headers['x-guest-token'] = r.text.split("gt=")[1].split(';')[0]

        url_flow_1 = "https://api.twitter.com/1.1/onboarding/task.json?flow_name=login"
        url_flow_2 = "https://api.twitter.com/1.1/onboarding/task.json"
        # Flow 1
        data = {'' : ''}
        r = requests.post(url_flow_1, headers=headers, data=json.dumps(data), proxies=proxies)
        flow_token = json.loads(r.text)['flow_token']
        cookie = ';'.join(['%s=%s' % (name, value) for (name, value) in r.cookies.get_dict(domain=".twitter.com").items()])
        print(success_color(f"[*] flow_token: {flow_token}"))

        # Flow 2
        data = {'flow_token' : flow_token, "subtask_inputs" : []}
        headers['cookie'] = cookie
        r = requests.post(url_flow_2, headers=headers, json=data, proxies=proxies)
        flow_token = json.loads(r.text)['flow_token']
        print(success_color(f"[*] flow_token: {flow_token}"))

        # Flow 3
        data = {"flow_token": flow_token ,"subtask_inputs":[{"subtask_id":"LoginEnterUserIdentifierSSO","settings_list":{"setting_responses":[{"key":"user_identifier","response_data":{"text_data":{"result":username}}}],"link":"next_link"}}]}
        r = requests.post(url_flow_2, headers=headers, json=data, proxies=proxies)
        flow_token = json.loads(r.text)['flow_token']
        print(success_color(f"[*] flow_token: {flow_token}"))

        # Flow 4
        data = {"flow_token": flow_token ,"subtask_inputs":[{"subtask_id":"LoginEnterPassword","enter_password":{"password":password,"link":"next_link"}}]}
        r = requests.post(url_flow_2, headers=headers, json=data, proxies=proxies)
        flow_token = json.loads(r.text)['flow_token']
        print(success_color(f"[*] flow_token: {flow_token}"))
    
        # lấy cookie đã đăng nhập để tương tác sau này
        cookie = ';'.join(['%s=%s' % (name, value) for (name, value) in r.cookies.get_dict(domain=".twitter.com").items()])
        # lấy mã x_csrf_token đã đăng nhập để tương tác sau này
        x_csrf_token = r.cookies['ct0']
        return x_csrf_token, cookie
    except Exception as e:
        return {"error": f"lỗi không xác định khi đăng nhập twitter, mã lỗi {e}"}