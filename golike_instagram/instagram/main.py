import colorama
import time
import json
import os
import requests
from golike_features import (
    get_jobs,
    drop_job,
    verify_complete_job,
    check_instagram_account_id,
    GOLIKE_HEADERS
)
from instagram_interection import (
    follow_instagram,
    like_instagram
)
from login_instagram import (
    login_instagram
)
import one_tk
import lg_get_ck
from fake_interaction import send_random_fake_requests
colorama.init()
import cloudscraper
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


# make waiting animation theme
def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(colorama.Fore.YELLOW + f"\r[{i}s] " + colorama.Style.RESET_ALL, end="")
        print(colorama.Fore.BLUE + text + colorama.Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0


def storage_block_account(username, path_block="./blocked_account.json"):
    try:
        if not os.path.exists(path_block):
            with open(path_block, "w") as file:
                json.dump({username: 0}, file)
        else:
            with open(path_block, "r") as file:
                blocked_accounts = json.load(file)
            if username in blocked_accounts:
                blocked_accounts[username] += 1
                print(system_color(f"[*] đã tăng thành công điểm gỡ bỏ hạn chế của -> {username}"))
            else:
                blocked_accounts[username] = 0
                print(system_color(f"[*] đã gán thành công điểm gỡ bỏ hạn chế cho -> {username}"))
            with open(path_block, "w") as file:
                json.dump(blocked_accounts, file)
        return {"success": f"đã lưu thành công account -> {username} vào danh sách hạn chế"}
    except:
        return {"error": "đã có lỗi khi lưu account vào danh sách hạn chế"}
    

def check_and_freedom_for_blocked_account(username, max_times_for_block_account, path_block="./blocked_account.json"):
    try:
        if not os.path.exists(path_block):
            return {"success": "chưa có account nào bị block để check"}
        else:
            with open(path_block, "r") as file:
                blocked_accounts = json.load(file)
            if username in blocked_accounts:
                if blocked_accounts[username] > max_times_for_block_account:
                    blocked_accounts.pop(username)
                    with open(path_block, "w") as file:
                        json.dump(blocked_accounts, file)
                        return {"success": f"đã gỡ hạn chế cho -> {username}"}
                else:
                    blocked_accounts[username] += 1
                    with open(path_block, "w") as file:
                        json.dump(blocked_accounts, file)
                    return {"blocking": f"tài khoản {username} vẫn còn trong phạm vi hạn chế"}
            else:
                return {"success": f"tài khoản {username} không có trong danh sách hạn chế"}
    except:
        return {"error": "có lỗi khi check và gỡ hạn chế cho accounts"}


# run automation get job and follow instagram and golike
def golike_instagram_auto(instagram_golike_id_input, cookies_inp, wait_time, current_account,
proxy: bool = True, max_times: int = 20, maxcount=5, sendtimes=5, fake_rqs_waitime=2, max_times_for_block_account=10):
    for _ in range(max_times):
        # print current work instagram account
        print(system_color(f"[0] account đang làm việc hiện tại là -> {current_account}"))
        
        # kiểm tra và gỡ hạn chế nếu đủ điều kiện
        o = check_and_freedom_for_blocked_account(current_account, max_times_for_block_account)
        if "success" in o:
            print(success_color(f"[*] {o['success']}"))
        elif "blocking" in o:
            print(error_color(f"[!] {o['blocking']}"))
            waiting_ui((sendtimes*fake_rqs_waitime)+wait_time, f"-> vui lòng chờ đợi {(sendtimes*fake_rqs_waitime)+wait_time}s")
            return {"error": o['blocking']}
        else:
            print(error_color(f"[!] {o['error']}"))

        # send fake requests for simulator real browser
        send_random_fake_requests(current_account, cookies_inp, sendtimes, fake_rqs_waitime)
        
        # trying again error when get job
        r_get_jobs = None
        count = 1
        err = False
        while count < maxcount:
            r_get_jobs = get_jobs(instagram_golike_id_input) # get job from golike
            # if error will return this function
            if "error" in r_get_jobs:
                print(error_color(f"\r[!] đã có lỗi khi nhận job, thử nhận lại"))
                waiting_ui(5, f"đã thử {count}/{maxcount} lần thử, đợi 5s...")
                err = True
            else:
                err = False
                break
            count += 1
        if err:
            print(error_color("[!] đã hết số lần thử!"))
            return {"error_not_import": r_get_jobs['error']}
        else:
            print(success_color("[*] đã nhận job thành công mà không có bất kỳ lỗi nào!"))
        
        # skip this job if job type is not follow
        if r_get_jobs[2].strip().lower() == "follow":
            # print the target and follow target
            print(purple_color(f"[#] mục tiêu -> {r_get_jobs[0]} (follow)"))
            follow_like_output = follow_instagram(current_account, r_get_jobs[0], r_get_jobs[3], cookies=cookies_inp, proxy=proxy)
            
            if 'following_status' in follow_like_output:
                if follow_like_output['following_status']:
                    print(success_color("[$] đã follow thành công!"))
                elif follow_like_output['outgoing_request']:
                    print(purple_color("[#] đã follow nhưng cần chờ đối phương xác nhận"))

        elif r_get_jobs[2].strip().lower() == "like":
            # print the target and like target
            print(purple_color(f"[#] mục tiêu -> {r_get_jobs[0]} (like)"))
            follow_like_output = like_instagram(current_account, r_get_jobs[0], r_get_jobs[-1], cookies=cookies_inp, proxy=proxy)
            
            if 'is_final' in follow_like_output:
                if follow_like_output['is_final']:
                    print(success_color("[$] đã like thành công!"))

        else:
            print(error_color("[!] không phải nhiệm vụ follow và like"))
            drop_job_result = drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])
            if "success" in drop_job_result:
                print(success_color(f"[*] {drop_job_result['success']}"))
            else:
                print(error_color(f"[!] {drop_job_result['error']}"))
                return drop_job_result
            waiting_ui(5, "-> vui lòng chờ đợi 5 giây")
            continue
        
        # if follow status is have in follow output will continue check
        if 'following_status' in follow_like_output:
            # if these both params is false, can inference this account temp blocking follow by instagram
            if not follow_like_output['following_status'] and not follow_like_output['outgoing_request']:
                drop_job_result = drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])
                if "success" in drop_job_result:
                    print(success_color(f"[*] {drop_job_result['success']}"))
                else:
                    print(error_color(f"[!] {drop_job_result['error']}"))
                    return drop_job_result
                # lưu trữ account đã bị chặn vào file cục bộ để giảm tương tác
                o = storage_block_account(current_account)
                if "success" in o:
                    print(success_color(f"[*] {o['success']}"))
                else:
                    print(error_color(f"[!] {o['error']}"))
                return {"error": "account instagram này đã bị chặn like/follow, vui lòng đổi tài khoản mới"}
        # if follow status is have in follow output will continue check
        elif 'is_final' in follow_like_output:
            # if these both params is false, can inference this account temp blocking follow by instagram
            if not follow_like_output['is_final']:
                drop_job_result = drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])
                if "success" in drop_job_result:
                    print(success_color(f"[*] {drop_job_result['success']}"))
                else:
                    print(error_color(f"[!] {drop_job_result['error']}"))
                    return drop_job_result
                # lưu trữ account đã bị chặn vào file cục bộ để giảm tương tác
                o = storage_block_account(current_account)
                if "success" in o:
                    print(success_color(f"[*] {o['success']}"))
                else:
                    print(error_color(f"[!] {o['error']}"))
                return {"error": "account instagram này đã bị chặn like/follow, vui lòng đổi tài khoản mới"}
        # skip job if target in job is not found
        elif "page_not_found" in follow_like_output:
            drop_job_result = drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])
            if "success" in drop_job_result:
                print(success_color(f"[*] {drop_job_result['success']}"))
            else:
                print(error_color(f"[!] {drop_job_result['error']}"))
                return drop_job_result
            waiting_ui(wait_time, f"-> vui lòng chờ đợi {wait_time}s")
            continue
        # unknow error
        elif "error" in follow_like_output:
            drop_job_result = drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])
            if "success" in drop_job_result:
                print(success_color(f"[*] {drop_job_result['success']}"))
            else:
                print(error_color(f"[!] {drop_job_result['error']}"))
                return drop_job_result
            return {"error": "account bị chặn hoặc lỗi không xác định"}
        
        # waiting 10s for verify job and get money
        waiting_ui(10, "-> vui lòng chờ đợi 10s để xác minh job")
        output = verify_complete_job(r_get_jobs[1], instagram_golike_id_input) # verify job
        # if error in verify job output, will skip this job and waiting for try again with new job
        if "error" in output:
            print(error_color(f"[!] {output['error']}"))
            drop_job_result = drop_job(r_get_jobs[1], r_get_jobs[3], instagram_golike_id_input, r_get_jobs[2])
            if "success" in drop_job_result:
                print(success_color(f"[*] {drop_job_result['success']}"))
            else:
                print(error_color(f"[!] {drop_job_result['error']}"))
                return drop_job_result
            waiting_ui(wait_time, f"vui lòng chờ đợi {wait_time}s")
            continue
        # else print output verify job status and continue do new jobs
        else:
            print(success_color(f"[$$] {output[1]}"))
            print(success_color(f"[$$] {output[2]}"))
            waiting_ui(wait_time, f"-> vui lòng chờ đợi {wait_time}s")
            continue
    else:
        print(success_color("[$] đã hết số lần tối đa trên mỗi account, sẽ đổi tài khoản và tiếp tục"))



# auto switch account and wait if many errs
def golike_instagram_auto_switch_account(IDs, PASSWORDS, nicknames, wait_time, proxy_interaction, max_times_inp, waitime_when_error=1200, path_err="./account_error.txt", maxcount=5, sendtimes=5, fake_rqs_waitime=2):
    # loop activing forever
    sum_login_error = 0
    sum_activate_error = 0
    while True:
        # loop for check and run job on list account linking on golike
        for i in range(len(IDs)):
            cookies = None
            # try login and get sessions with password saved
            login_error = False
            for passwd in PASSWORDS:
                login_output = login_instagram(nicknames[i], passwd, proxy_interaction)
                if "error" in login_output:
                    sum_login_error += 1
                    print(error_color(f"[!] {login_output['error']}"))
                    waiting_ui(timeout=5, text="-> đợi 5s để tiếp tục")
                    login_error = True
                    continue
                else:
                    sum_login_error = 0
                    print(success_color(f"[*] {login_output['success']}"))
                    cookies = login_output['cookies']
                    login_error = False
                    break
            # save error account into log
            if login_error:
                with open(path_err, "a") as file:
                    file.write(f"{nicknames[i]}\n")
            # if cookies is None can inference is this account is blocked or failed login for get cookies
            # so let's skip this account
            if cookies is None:
                if sum_login_error >= (len(IDs)-2) * len(PASSWORDS):
                    waiting_ui(timeout=waitime_when_error, text=f"-> vui lòng đợi {waitime_when_error}s để check lại và chạy follow cho tất cả tài khoản")
                    sum_login_error = 0
                else:
                    sum_login_error += 1
                    waiting_ui(5, "-> đợi 5s để tiếp tục")
                continue
            # else (if cookies if not none) will run golike automation follow instagram and get money
            else:
                proxy_interaction = login_output['proxy'] if proxy_interaction else None
                golike_auto_output = golike_instagram_auto(IDs[i], cookies, wait_time, nicknames[i], proxy_interaction, max_times_inp, maxcount=maxcount, sendtimes=sendtimes, fake_rqs_waitime=fake_rqs_waitime)

                if golike_auto_output is None:
                    sum_activate_error = 0
                    continue

                elif "error" in golike_auto_output:
                    sum_activate_error += 1
                    print(error_color(f"[!] {golike_auto_output['error']}"))

                elif "error_not_import" in golike_auto_output:
                    print(error_color(f"[!] {golike_auto_output['error_not_import']}"))
                    sum_activate_error += 1

                if sum_activate_error > len(IDs) - 2:
                    waiting_ui(timeout=waitime_when_error, text=f"-> vui lòng đợi {waitime_when_error}s để check lại và chạy follow cho tất cả tài khoản")
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




# get golike username instagram and account id
def get_golike_instagram_usernames():
    # print and storage IDs and Nicknames
    print()
    print(system_color("[#] các ID instagram trên golike của bạn ↓"))

    IDs = []
    nicknames = []

    nickname_id_result = check_instagram_account_id()
    maxlen = max([len(nickname[1]) for nickname in nickname_id_result]) + 25
    print(system_color(" -" + ((maxlen-1) * "-") ))
    
    for nickname_id in nickname_id_result:
        nickname_id_z = f"| id -> {nickname_id[0]}"
        nickname_id_o = f"| instagram username -> {nickname_id[1]}"
        for _ in range(len(nickname_id_z), maxlen):
            nickname_id_z += " "
        for _ in range(len(nickname_id_o), maxlen):
            nickname_id_o += " "
        nickname_id_z += "|"
        nickname_id_o += "|"
        print(success_color(nickname_id_z))
        print(success_color(nickname_id_o))
        print(system_color(" -" + ((maxlen-1) * "-") ))

        IDs.append(nickname_id[0])
        nicknames.append(nickname_id[1])
    return IDs, nicknames




# golike instagram UI
def golike_instagram_ui(golike_author_path: str = "./golike_author.json"):
    global GOLIKE_HEADERS
    PASSWORDS = json.load(open("./password.json"))
    PASSWORDS = PASSWORDS['passwords']

    # golike author read and write
    golike_add_author_ui(golike_author_path)
    storage_golike_author(golike_author_path)
    IDs, nicknames = get_golike_instagram_usernames()
    print()
    
    # get waitime for next job from user input
    wait_time = int(input(system_color("[?] nhập số thời gian chờ trước khi follow tiếp theo\n-> ")))
    # max times for interaction on account
    max_times_inp = int(input(system_color("[?] nhập vào số lần tối đa mà một account có thể tương tác\n-> ")))
    # wait time when error too much
    waitime_when_error = int(input(system_color("[?] nhập vào số thời gian chờ tối đa khi bị lỗi quá nhiều\n-> ")))
    maxcount = int(input(system_color("[?] số lần tối đa để thử lại nhận job\n-> ")))
    sendtimes = int(input(system_color("[?] nhập số lần gửi các yêu cầu mô phỏng\n-> ")))
    fake_rqs_waitime = int(input(system_color("[?] nhập vào thời gian chờ cho lần gửi rqs mô phỏng tiếp theo\n-> ")))
    # ask about using proxy in activing progress or not
    proxy_choose_interaction = input(system_color("[?] bạn có muốn dùng proxy trong quá trình tương tác instagram không?(Y/n)\n-> "))
    print()
    
    if proxy_choose_interaction.strip().lower() == "y":
        print(success_color("[!] bạn đã lựa chọn là sử dụng proxy trong quá trình tương tác"))
        proxy_interaction = True
    else:
        print(error_color("[1] bạn đã lựa chọn là không sử dụng proxy trong quá trình tương tác"))
        proxy_interaction = None
    
    print(system_color("[!] bạn có thể dùng CTRL+C để thoát khỏi chương trình và quay về console"))
    waiting_ui(2, "-> đợi 2 giây để chạy tool")
    
    # run golike auto and auto switch accounts
    print()
    print()
    try:
        golike_instagram_auto_switch_account(IDs, PASSWORDS, nicknames, wait_time, proxy_interaction, max_times_inp, waitime_when_error=waitime_when_error, maxcount=maxcount, sendtimes=sendtimes, fake_rqs_waitime=fake_rqs_waitime)
    except KeyboardInterrupt:
        print(success_color("[#] đã nhận CTRL+C, quay lại..."))




# add more password for instagram
def add_passwords_ui():
    while True:
        try:
            print(purple_color("[!] nhập lệnh exit nếu bạn muốn thoát khỏi!"))
            passwd_inp = input(system_color("[?] nhập password chung bạn muốn thêm\n-> "))
            
            # exit the terminal for add passwords
            if passwd_inp.lower().strip() == "exit":
                print(system_color("[*] bạn đã thoát khỏi trình thêm passwords!"))
                print()
                break
            
            # add new password in file
            if os.path.exists("./password.json"):
                passwords = json.load(open("./password.json", "r"))
                passwords['passwords'].append(passwd_inp)
            else:
                passwords = {"passwords": [passwd_inp]}
            json.dump(passwords, open("./password.json", 'w'))
            print(success_color(f"[*] đã thêm password -> '{passwd_inp}' thành công!"))
            print()
        except Exception as e:
            print(error_color(f"[!] đã có lỗi khi thêm password -> '{passwd_inp}'!"))




def print_passwords_table(screen_wait=False):
    passwords = json.load(open("./password.json", "r"))
    passwords = passwords['passwords']

    if str(passwords) == "[]":
        input(system_color("[!] không có passwords chung nào hiện có! enter để quay lại console chính\n-> "))
        return 0 
                
    maxlen = max([len(passwords[i]) for i in range(len(passwords))]) + 15

    print(system_color("[*] danh sách các passwords chung hiện có bên dưới ↓"))
    print(system_color(" -" + ((maxlen-1) * "-") ))
    for i in range(len(passwords)):
        password = f"| [{i+1}] -> {passwords[i]}"
        for _ in range(len(password), maxlen):
            password += " "
        password += '|'
        print(system_color(password))
    print(system_color(" -" + ((maxlen-1) * "-") ))

    if screen_wait:
        print()
        input(system_color("[#] nhấn enter để quay lại\n-> "))
        



def delete_passwords_ui():
    if os.path.exists("./password.json"):
        passwords = json.load(open("./password.json", "r"))
        if str(passwords['passwords']) != "[]":
            passwords = passwords['passwords']

            print_passwords_table()

            print()
            while True:
                choose_password_delete = input(system_color("[?] nhập password bạn muốn xóa hoặc gõ 'clear' để xóa tất cả\n-> "))

                if choose_password_delete.strip().lower() == "clear":
                    json.dump({"passwords": []}, open("./password.json", "w"))
                    input(system_color("[!] không có passwords chung nào hiện có! enter để quay lại console chính\n-> "))
                    return 0 
                try:
                    choose_password_delete = int(choose_password_delete)
                except:
                    print(error_color("[!] vui lòng nhập số thứ tự tương ứng!"))
                    print()

                passwd_hist = passwords[choose_password_delete-1]
                try:
                    passwords.pop(choose_password_delete-1)
                    json.dump({"passwords": passwords}, open("./password.json", "w"))
                    print(success_color(f"[*] đã xóa passwords -> {passwd_hist} thành công!"))
                    print()
                    print_passwords_table()
                except Exception as e:
                    print(error_color(f"[!] xóa passwords -> {passwd_hist} không thành công!"))
                    print()
                    print_passwords_table()
        else:
            input(system_color("[!] không có passwords chung nào hiện có! enter để quay lại console chính\n-> "))




def add_username_password_instagram(path="./instgaram_cookies.json"):
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


# main program
if __name__ == "__main__":
    while True:
        if not os.path.exists("./password.json"):
            choose = input(system_color("[?] file 'password.json' chưa có, bạn muốn tạo? (Y/n)\n-> "))
            if choose.strip().lower() == "y":
                print(purple_color("[!] tạo file 'password.json' ..."))
                with open("password.json", "w") as file:
                    json.dump({"passwords": []}, open("./password.json", "w"))
                    print(success_color("[@] tạo file 'password.json' thành công"))
            else:
                exit()
                
        print(system_color(" --------------------------------------------"))
        print((system_color("|")+success_color(" TOOL GOLIKE INSTAGRAM AUTO 100% BY PHUTECH ")+system_color("|")))
        print(system_color("| facebook -> Programing Sama                |"))
        print(system_color("| youtube -> Phu Tech                        |"))
        print(system_color("| github -> @phucoding286                    |"))
        print(system_color(" --------------------------------------------"))
        print(system_color("| [1] chạy tool golike tự động cho instagram |"))
        print(system_color("| [2] thêm các passwords chung cho instagram |"))
        print(system_color("| [3] xóa các passwords chung của instagram  |"))
        print(system_color("| [4] xem các passwords chung hiện đang lưu  |"))
        print(system_color("| [5] thêm thông tin instagram vào database  |"))
        print(system_color("| [6] chế độ một tài khoản                   |"))
        print(system_color("| [7] đăng nhập và lấy cookie instagram      |"))
        print(system_color(" --------------------------------------------"))
        print()
        print(system_color("[!] các chức năng chính ↓"))
        print(success_color(" -> tự động đăng nhập và tương tác instagram"))
        print(success_color(" -> tự động nhận job và xác minh job golike"))
        print(success_color(" -> tự động chờ khi có quá nhiều lần chặn hoặc lỗi"))
        print(success_color(" -> tự động giả mạo các thông tin để giảm thiểu nghi ngờ"))
        print()

        choose_inp = input(system_color("[|] nhập lựa chọn của bạn\n-> "))
        print()

        if choose_inp.strip().lower() == "1":
            golike_instagram_ui()
            print()
        elif choose_inp.strip().lower() == "2":
            add_passwords_ui()
            print()
        elif choose_inp.strip().lower() == "3":
            delete_passwords_ui()
            print()
        elif choose_inp.strip().lower() == "4":
            print_passwords_table(True)
            print()
        elif choose_inp.strip().lower() == "5":
            add_username_password_instagram()
            print()
        elif choose_inp.strip().lower() == "6":
            one_tk.main()
            print()
        elif choose_inp.strip().lower() == "7":
            lg_get_ck.lg_get_ck()
        else:
            print(error_color("[!] vui lòng nhập đúng số thứ tự"))
            print()
            time.sleep(1)