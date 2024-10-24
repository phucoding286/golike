from colorama import Fore, Style
import time
import colorama
from tw_login import login_twitter
from get_job_golike import (
    check_tw_account_id,
    get_jobs,
    drop_job,
    verify_complete_job,
    GOLIKE_HEADERS
)
from tw_interactions import tw_follow
import json
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

def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(Fore.YELLOW + f"\r{i}s " + Style.RESET_ALL, end="")
        print(Fore.BLUE + text + Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0



def golike_tw_auto(id_golike_tw, x_csrf_token, cookie, wait_time, nickname, proxy, max_times):
    for _ in range(max_times):
        print(system_color(f"account đang làm việc hiện tại là: -> {nickname}"))
        r_get_job = get_jobs(id_golike_tw)

        if "error" in r_get_job:
            print(error_color(str(r_get_job['error'])))
            waiting_ui(5, "đợi 5s để tiếp tục")
            return {"error_not_import": r_get_job['error']}

        if r_get_job[2].strip().lower() == "follow":
            target_link = r_get_job[0]
            follow_output = tw_follow(cookie, x_csrf_token, r_get_job[3], target_link, proxy)
            print(purple_color(follow_output))
        else:
            print(error_color("job khác follow nên sẽ bỏ qua"))
            print(drop_job(r_get_job[1], r_get_job[3], id_golike_tw))
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
            print(drop_job(r_get_job[1], r_get_job[3], id_golike_tw))
            waiting_ui(wait_time, "đợi 60s để tiếp tục")
            continue
        else:
            print("xác minh job thành công")
            print(success_color(str(vrf_output)))
            waiting_ui(wait_time, "đợi 60s để tiếp tục")



def golike_auto_tw_main():
    authorization_inp = input(system_color("nhập vào authorization golike của bạn\n>>> "))
    GOLIKE_HEADERS['Authorization'] = authorization_inp
    golike_token_input = input(system_color("nhập token golike của bạn\n>>> "))
    GOLIKE_HEADERS['t'] = golike_token_input
    PASSWORDS = json.load(open("./password.json"))
    PASSWORDS = PASSWORDS['passwords']

    # print and storage IDs and Nicknames
    print(system_color("các id của bạn là:"))
    count = 1
    IDs = []
    nicknames = []
    for nickname_id in check_tw_account_id():
        print(success_color(f"{count}. id: {nickname_id[0]} tw username: {nickname_id[1]}"))
        count += 1
        IDs.append(nickname_id[0])
        nicknames.append(nickname_id[1])
    
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

    # loop activing forever
    sum_login_error = 0
    sum_activate_error = 0
    while True:
        # loop for check and run job on list account linking on golike
        for i in range(len(IDs)):
            cookies = None
            x_csrf_token = None
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
                    cookies = login_output[1]
                    x_csrf_token = login_output[0]
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
                golike_auto_output = golike_tw_auto(IDs[i], x_csrf_token, cookies, wait_time, nicknames[i], proxy_interaction, max_times_inp)
                
                if golike_auto_output is None:
                    sum_activate_error = 0
                    continue
                
                elif "error" in golike_auto_output:
                    sum_activate_error += 1
                    print(error_color(golike_auto_output['error']))
                    if sum_activate_error > len(IDs) - 2:
                        waiting_ui(timeout=1200, text="vui lòng đợi 20p (1200s) để check lại và chạy follow cho tất cả tài khoản")
                        sum_activate_error = 0

                elif "error_not_import" in golike_auto_output:
                    print(error_color(golike_auto_output['error_not_import']))
                    sum_activate_error += 1


if __name__ == "__main__":
    golike_auto_tw_main()