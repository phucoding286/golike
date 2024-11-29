from colorama import Fore, Style
import time
import colorama
from tw_login import login_twitter
from get_job_golike import (
    check_tw_account_id,
    get_job,
    drop_job,
    verify_complete_job,
    GOLIKE_HEADERS
)
from tw_interactions import tw_follow
import json
import cloudscraper
import os
colorama.init()

scraper = cloudscraper.create_scraper()

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

def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(Fore.YELLOW + f"\r{i}s " + Style.RESET_ALL, end="")
        print(Fore.BLUE + text + Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0



def golike_tw_auto(id_golike_tw, cookie, wait_time, nickname, proxy, max_times):
    for _ in range(max_times):
        print(system_color(f"account đang làm việc hiện tại là: -> {nickname}"))
        r_get_job = get_job(id_golike_tw)

        if "error" in r_get_job:
            print(error_color(str(r_get_job['error'])))
            waiting_ui(5, "đợi 5s để tiếp tục")
            return {"error_not_import": r_get_job['error']}

        if r_get_job[2].strip().lower() == "follow":
            target_link = r_get_job[0]
            follow_output = tw_follow(cookie, r_get_job[3], target_link, proxy)
            print(purple_color(follow_output))
        else:
            print(error_color("job khác follow nên sẽ bỏ qua"))
            print(error_color(drop_job(r_get_job[1], r_get_job[3], id_golike_tw)))
            waiting_ui(5, "đợi 5s để tiếp tục")
            continue

        if "following" not in follow_output:
            print(error_color("không follow thành công, sẽ bỏ qua"))
            print(success_color(drop_job(r_get_job[1], r_get_job[3], id_golike_tw)))
            waiting_ui(wait_time, "đợi 60s để tiếp tục")
            continue
    
        vrf_output = verify_complete_job(r_get_job[1], id_golike_tw)
        if "error" in vrf_output:
            print(error_color(str(vrf_output['error'])))
            print(error_color(drop_job(r_get_job[1], r_get_job[3], id_golike_tw)))
            waiting_ui(wait_time, "đợi 60s để tiếp tục")
            continue
        else:
            print(success_color(str(vrf_output)))
            waiting_ui(wait_time, "đợi 60s để tiếp tục")


# auto switch account and wait if many errs
def golike_tw_auto_switch_account(IDs, PASSWORDS, nicknames, proxy_login, wait_time, proxy_interaction, max_times_inp):
    # loop activing forever
    sum_login_error = 0
    sum_activate_error = 0
    while True:
        # loop for check and run job on list account linking on golike
        for i in range(len(IDs)):
            cookies = None
            # try login and get sessions with password saved
            for passwd in PASSWORDS:
                login_output = login_twitter(nicknames[i], passwd, proxy_login)
                if "error" in login_output:
                    sum_login_error += 1
                    print(error_color(login_output['error']))
                    waiting_ui(timeout=5, text="đợi 5s để tiếp tục")
                    continue
                else:
                    sum_login_error = 0
                    print(success_color("login twitter thành công"))
                    cookies = login_output['cookies']
                    break
            # if cookies is None can inference is this account is blocked or failed login for get cookies
            # so let's skip this account
            if cookies is None:
                if sum_login_error >= len(IDs) - 2:
                    waiting_ui(timeout=1200, text="vui lòng đợi 20p (1200s) để check lại và chạy follow cho tất cả tài khoản")
                    sum_login_error = 0
                else:
                    sum_login_error += 1
                    waiting_ui(5, "đợi 5s để tiếp tục")
                continue
            # else (if cookies if not none) will run golike automation follow instagram and get money
            else:
                
                golike_auto_output = golike_tw_auto(IDs[i], cookies, wait_time, nicknames[i], proxy_interaction, max_times_inp)

                if golike_auto_output is None:
                    sum_activate_error = 0
                    continue
                
                elif "error" in golike_auto_output:
                    sum_activate_error += 1
                    print(error_color(golike_auto_output['error']))

                elif "error_not_import" in golike_auto_output:
                    print(error_color(golike_auto_output['error_not_import']))
                    sum_activate_error += 1

                if sum_activate_error > len(IDs) - 2:
                    waiting_ui(timeout=1200, text="vui lòng đợi 20p (1200s) để check lại và chạy follow cho tất cả tài khoản")
                    sum_activate_error = 0
                    continue

# storage golike author, token in local file for using later
def storage_golike_author(golike_author_path: str = "./golike_author.json"):
    # send the requests check account id but just get username golike for storage author data
    resj = None
    while True:
        try:
            response = scraper.get(
                url="https://gateway.golike.net/api/instagram-account",
                headers=GOLIKE_HEADERS
            )
            resj = response.json()
            break
        except:
            print(error_color("[!] đã có lỗi khi gửi yêu cầu check id, thử lại.."))
            continue

    # save golike author data in hist for using again then
    if not os.path.exists(golike_author_path):
        with open(golike_author_path, "w") as file:
            json.dump({}, file)
    with open(golike_author_path, "r") as file:
        author_data = json.load(file)
    if resj['data'][0]['username'] not in author_data:
        author_data[resj['data'][0]['username']] = {'authorization': GOLIKE_HEADERS['Authorization'], "token": GOLIKE_HEADERS['t']}
        with open(golike_author_path, "w") as file:
            json.dump(author_data, file)

# add author golike, token for run program
def golike_add_author_ui(golike_author_path: str = "./golike_author.json"):
    author_data = {}
    if os.path.exists(golike_author_path):
        with open(golike_author_path, "r") as file:
            author_data = json.load(file)
    
    choose = None
    golike_usernames = []
    if str(author_data) != "{}":
        print(system_color("[*] đã có sẵn tài khoản golike đã chạy lần trước ↓"))
        maxlen = max([len(key) for key in author_data.keys()]) + 25
        print(" -" + ((maxlen-2) * system_color("-")))
        count = 1
        for key, value in author_data.items():
            golike_usernames.append(key)
            key = f"| [{count}] username golike -> {key}"
            for _ in range(len(key), maxlen):
                key += " "
            key += "|"
            print(success_color(key))
            count += 1
        print(" -" + ((maxlen-2) * system_color("-")))
        print()
        
        while True:
            choose = input(system_color("[?] đã có account golike đã lưu, nhấp chọn hoặc gõ 'q' để thoát và thêm author mới\n-> "))
            if choose.strip().lower() == "q":
                break
            try:
                choose = int(choose) - 1
                break
            except:
                print(error_color("[!] vui lòng nhập đúng số thứ tự!"))

    if choose is None or isinstance(choose, str) and choose.strip().lower() == "q":
        # get golike authorization from user input
        golike_authorization_input = input(system_color("[?] nhập authorization golike của bạn\n-> "))
        GOLIKE_HEADERS['Authorization'] = golike_authorization_input
        # get golike token from user input
        golike_token_input = input(system_color("[?] nhập token golike của bạn\n-> "))
        GOLIKE_HEADERS['t'] = golike_token_input
    else:
        GOLIKE_HEADERS['Authorization'] = author_data[golike_usernames[choose]]['authorization']
        GOLIKE_HEADERS['t'] = author_data[golike_usernames[choose]]['token']


# golike auto main process
def golike_auto_tw_main():
    global GOLIKE_HEADERS
    PASSWORDS = json.load(open("./password.json"))
    PASSWORDS = PASSWORDS['passwords']

    # golike author read and write
    golike_add_author_ui()
    storage_golike_author()

    # print and storage IDs and Nicknames
    print(system_color("\ncác id của bạn là:"))
    count = 1
    IDs = []
    nicknames = []
    for nickname_id in check_tw_account_id():
        print(success_color(f"{count}. id: {nickname_id[0]} tw username: {nickname_id[1]}"))
        count += 1
        IDs.append(nickname_id[0])
        nicknames.append(nickname_id[1])
    print()
    
    # get waitime for next job from user input
    wait_time = int(input(system_color("Nhập số thời gian chờ trước khi follow tiếp theo\n>>> ")))

    # max times for interaction on account
    max_times_inp = int(input(system_color("nhập vào số lần tối đa mà một account có thể tương tác\n>>> ")))

    # ask about using proxy in activing progress or not
    proxy_choose_login = input(system_color("Bạn có muốn dùng proxy trong quá trình login twitter không?(Y/n)\n>>> "))
    proxy_choose_interaction = input(system_color("Bạn có muốn dùng proxy trong quá trình tương tác twitter không?(Y/n)\n>>> "))
    
    if proxy_choose_login.strip().lower() == "y":
        print(success_color("bạn đã lựa chọn là sử dụng proxy trong quá trình đăng nhập"))
        proxy_login = True
    else:
        print(error_color("bạn đã lựa chọn là không sử dụng proxy trong quá trình đăng nhập"))
        proxy_login = False
    if proxy_choose_interaction.strip().lower() == "y":
        print(success_color("bạn đã lựa chọn là sử dụng proxy trong quá trình tương tác"))
        proxy_interaction = True
    else:
        print(error_color("bạn đã lựa chọn là không sử dụng proxy trong quá trình tương tác"))
        proxy_interaction = False

    # run golike auto and auto switch accounts
    golike_tw_auto_switch_account(IDs, PASSWORDS, nicknames, proxy_login, wait_time, proxy_interaction, max_times_inp)


def add_username_password_twitter(path="./twitter_cookies.json"):
    with open(path, "r") as file:
        instagram_cookies = json.load(file)
    while True:
        print(purple_color("[*] bạn có thể nhập 'exit' để thoát"))
        username = input(system_color("[?] nhập vào username bạn cần truy vấn\n-> "))
        if username.strip().lower() == "exit":
            print(success_color("[*] bạn đã chọn thoát chương trình này"))
            return 0
        if username not in instagram_cookies:
            choose = input(success_color(f"[!] username {username} chưa tồn tại trong database, muốn thêm? (Y/n)\n-> "))
            if choose.strip().lower() == "y":
                print(system_color(f"[*] bạn đã lựa chọn thêm username -> {username}"))
                password = input(system_color(f"[?] nhập password cho username -> {username}\n[{username}]> "))
                cookies = input(system_color(f"[?] nhập cookies cho username (enter mặc định trống)\n[{username}]> "))
                instagram_cookies[username] = {"username": username, "password": password, "cookie": cookies, "proxy": None}
                try:
                    with open(path, "w") as file:
                        json.dump(instagram_cookies, file)
                    print(success_color(f"[*] đã lưu thông tin cho username {username} thành công"))
                    print()
                except:
                    print(error_color(f"[*] bị lỗi khi lưu thông tin cho username {username}!"))
                    print()
            else:
                print()
                continue
        else:
            if "username" not in instagram_cookies[username] or "password" not in instagram_cookies[username]:
                choose = input(system_color(f"[!] username {username} đã tồn tại trong database nhưng chưa có thông tin, muốn thêm? (Y/n)\n-> "))
                if choose.strip().lower() == "y":
                    password = input(system_color(f"[?] nhập password cho username -> {username}\n[{username}]> "))
                    cookies = input(system_color(f"[?] nhập cookies cho username (enter mặc định trống)\n[{username}]> "))
                    info = {"username": username, "password": password}
                    if "cookie" in instagram_cookies[username]:
                        info["cookie"] = instagram_cookies[username]['cookie']
                    else:
                        info["cookie"] = cookies
                    if "proxy" in instagram_cookies[username]:
                        info["proxy"] = instagram_cookies[username]['proxy']
                    else:
                        info['proxy'] = None
                    instagram_cookies[username] = info    
                    try:
                        with open(path, "w") as file:
                            json.dump(instagram_cookies, file)
                        print(success_color(f"[*] đã lưu thông tin cho username {username} thành công"))
                        print()
                    except:
                        print(error_color(f"[*] bị lỗi khi lưu thông tin cho username {username}!"))
                        print()
                else:
                    print()
                    continue
            else:
                print(success_color(f"[*] thông tin của {username} đã tồn tại rồi!"))
                choose = input(system_color("[?] bạn muốn chỉnh sửa mật khẩu?(Y/n)\n-> "))
                if choose.strip().lower() == "y":
                    while True:
                        print()
                        print(purple_color("[!] lưu ý! bạn có thể gõ 'exit' để thoát khỏi terminal"))
                        print(success_color(" -> gõ lệnh 'ls password' để xem các password hiện có"))
                        print(success_color(" -> gõ lệnh 'change' để đổi mật khẩu, ví dụ 'change abc123'"))
                        print()
                        terminal_input = input(system_color(f"[{username}]> "))
                        if terminal_input.lower().split()[0] == 'change':
                            try:
                                password = terminal_input.split()[1]
                            except:
                                print(error_color("[!] vui lòng nhập tham số khi đổi mật khẩu"))
                                continue
                            instagram_cookies[username]['password'] = password
                            try:
                                with open(path, "w") as file:
                                    json.dump(instagram_cookies, file)
                                print(success_color(f"[*] đã lưu mật khẩu '{password}' cho '{username}' thành công!"))
                            except:
                                print(error_color(f"[!] lưu mật khẩu '{password}' cho '{username}' thất bại!"))
                            print()
                            input(system_color("[*] enter để tiếp tục\n-> "))
                            print()
                        elif terminal_input.lower().strip() == "ls password":
                            print(purple_color(f"[#] password của account {username} -> {instagram_cookies[username]['password']}"))
                            print()
                            input(system_color("[*] enter để tiếp tục\n-> "))
                            print()
                        elif terminal_input.lower().strip() == "exit":
                            break
                continue


if __name__ == "__main__":
    while True:
        print(system_color('1. chạy tool twitter'))
        print(system_color('2. quản lý username, password twitter'))
        print()
        inp = input(system_color("nhập vào lựa chọn của bạn: "))
        if inp.lower().strip() == "1":
            golike_auto_tw_main()
        elif inp.lower().strip() == "2":
            add_username_password_twitter()
        else:
            print("vui lòng nhập đúng lựa chọn!")
            continue