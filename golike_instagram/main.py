import colorama
import time
import json
import os
from golike_features import (
    get_jobs,
    drop_job,
    verify_complete_job,
    check_instagram_account_id,
    GOLIKE_HEADERS
)
from instagram_interection import (
    follow_instagram
)
from login_instagram import (
    login_instagram
)
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
        print(colorama.Fore.YELLOW + f"\r{i}s " + colorama.Style.RESET_ALL, end="")
        print(colorama.Fore.BLUE + text + colorama.Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0


print(system_color("""
TOOL BY PHUTECH
"""))


# run automation get job and follow instagram and golike
def golike_instagram_auto(instagram_golike_id_input, cookies_inp, wait_time, current_account, proxy: bool = True):
    while True:
        # print current work instagram account
        print(system_color(f"account đang làm việc hiện tại là: {current_account}"))
        r_get_jobs = get_jobs(instagram_golike_id_input) # get job from golike
        # if error will return this function
        if "error" in r_get_jobs:
            return {"error": r_get_jobs['error']}
        # skip this job if job type is not follow
        if r_get_jobs[2] != "follow":
            print(error_color("không phải nhiệm vụ follow"))
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])))
            waiting_ui(1, "vui lòng chờ đợi 1 giây")
            continue
        
        # print the target and follow target
        print(purple_color(f"mục tiêu: {r_get_jobs[0]}"))
        follow_output = follow_instagram(r_get_jobs[0], r_get_jobs[3], cookies=cookies_inp, proxy=proxy)
        print(purple_color(follow_output))
        
        # if follow status is have in follow output will continue check
        if 'following_status' in follow_output:
            # if these both params is false, can inference this account temp blocking follow by instagram
            if not follow_output['following_status'] and not follow_output['outgoing_request']:
                print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])))
                return {"error": "account instagram này đã bị chặn follow, vui lòng đổi tài khoản mới"}
        # skip job if target in job is not found
        elif "page_not_found" in follow_output:
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])))
            waiting_ui(wait_time, f"vui lòng chờ đợi {wait_time}s")
            continue
        # unknow error
        elif "error" in follow_output:
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])))
            return {"error": "account bị chặn hoặc lỗi không xác định"}
        
        # waiting 10s for verify job and get money
        waiting_ui(10, "vui lòng chờ đợi 10s để xác minh job")
        output = verify_complete_job(r_get_jobs[1], instagram_golike_id_input) # verify job
        # if error in verify job output, will skip this job and waiting for try again with new job
        if "error" in output:
            print(success_color(drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])))
            waiting_ui(wait_time, f"vui lòng chờ đợi {wait_time}s")
            continue
        # else print output verify job status and continue do new jobs
        else:
            print(success_color(output))
            waiting_ui(wait_time, f"vui lòng chờ đợi {wait_time}s")
            continue



# golike instagram UI
def golike_instagram_ui():
    global GOLIKE_HEADERS
    # get golike authorization from user input
    golike_authorization_input = input(system_color("nhập authorization golike của bạn\n>>> "))
    GOLIKE_HEADERS['Authorization'] = golike_authorization_input
    # get golike token from user input
    golike_token_input = input(system_color("nhập token golike của bạn\n>>> "))
    GOLIKE_HEADERS['t'] = golike_token_input
    PASSWORDS = json.load(open("./golike_instagram/password.json"))
    PASSWORDS = PASSWORDS['passwords']
    
    # print and storage IDs and Nicknames
    print(system_color("các id của bạn là:"))
    count = 1
    IDs = []
    nicknames = []
    for nickname_id in check_instagram_account_id():
        print(success_color(f"{count}. id: {nickname_id[0]} instagram_username: {nickname_id[1]}"))
        count += 1
        IDs.append(nickname_id[0])
        nicknames.append(nickname_id[1])
    
    # get waitime for next job from user input
    wait_time = int(input(system_color("Nhập số thời gian chờ trước khi follow tiếp theo\n>>> ")))

    # ask about using proxy in activing progress or not
    proxy_choose = input(system_color("Bạn có muốn dùng proxy trong quá trình tương tác instagram không?(Y/n)\n>>> "))
    if proxy_choose.strip().lower() == "y":
        print(success_color("bạn đã lựa chọn là sử dụng proxy trong quá trình"))
        proxy = True
    else:
        print(error_color("bạn đã lựa chọn là không sử dụng proxy trong quá trình"))
        proxy = False

    # loop activing forever
    while True:
        sum_login_error = 0
        sum_activate_error = 0

        # loop for check and run job on list account linking on golike
        for i in range(len(IDs)):
            cookies = None
            # try login and get sessions with password saved
            for passwd in PASSWORDS:
                login_output = login_instagram(nicknames[i], passwd, proxy)
                if "error" in login_output:
                    print(error_color(login_output['error']))
                    waiting_ui(timeout=5, text="đợi 5s để tiếp tục")
                    continue
                else:
                    sum_login_error = 0
                    print(success_color(login_output['success']))
                    cookies = login_output['cookies']
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
                golike_auto_output = golike_instagram_auto(IDs[i], cookies, wait_time, nicknames[i], proxy)
                if "error" in golike_auto_output:
                    sum_activate_error += 1
                    print(error_color(golike_auto_output['error']))
                    if sum_activate_error > len(IDs) - 2:
                        waiting_ui(timeout=1200, text="vui lòng đợi 20p (1200s) để check lại và chạy follow cho tất cả tài khoản")
                        sum_activate_error = 0



# add more password for instagram
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


# main program
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
        elif choose_table == 1:
            add_passwords_ui()