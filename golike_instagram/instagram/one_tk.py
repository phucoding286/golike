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
    follow_instagram,
    like_instagram
)
from login_instagram import (
    login_instagram
)
from fake_interaction import send_random_fake_requests
colorama.init()
import cloudscraper
scraper = cloudscraper.create_scraper()


tryIfBlockCount = 0
maxTryIfBlock = 3

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



# run automation get job and follow instagram and golike
def golike_instagram_auto(instagram_golike_id_input, cookies_inp, wait_time, current_account, loop, maxcount=5):
    
    global tryIfBlockCount
    global maxTryIfBlock
    
    for _ in range(loop):

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
            follow_like_output = follow_instagram(current_account, r_get_jobs[0], r_get_jobs[3], cookies=cookies_inp, proxy=None)
            
            if 'following_status' in follow_like_output:
                if follow_like_output['following_status']:
                    print(success_color("[$] đã follow thành công!"))
                elif follow_like_output['outgoing_request']:
                    print(purple_color("[#] đã follow nhưng cần chờ đối phương xác nhận"))

        elif r_get_jobs[2].strip().lower() == "like":
            # print the target and like target
            print(purple_color(f"[#] mục tiêu -> {r_get_jobs[0]} (like)"))
            follow_like_output = like_instagram(current_account, r_get_jobs[0], r_get_jobs[-1], cookies=cookies_inp, proxy=None)
            
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
                
                if tryIfBlockCount >= maxTryIfBlock:
                    tryIfBlockCount = 0
                    return {"error": "account instagram này đã bị chặn like/follow, vui lòng đổi tài khoản mới"}
                else:
                    print(error_color("account instagram này đã bị chặn like/follow, sẽ thử lại thêm vài lần nữa"))
                    tryIfBlockCount += 1
                    continue

            else:
                tryIfBlockCount = 0

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
        return "[$] đã hết số lần tối đa trên mỗi account, sẽ đổi tài khoản và tiếp tục"


def main():
    golike_add_author_ui()
    id_ins_gol = input(system_color("[?] Nhập vào id instagram đang liên kết trên golike\n-> "))
    cookie_inp = input(system_color("[?] Nhập vào cookie instagram\n-> "))
    wait = int(input(system_color("[?] Nhập vào thời gian chờ đợi\n-> ")))
    tryJob = int(input(system_color("[?] Nhập vào số lần thử lại\n-> ")))
    loop = int(input(system_color("[?] Nhập vào số lần tương tác\n-> ")))
    username = ""
    output = golike_instagram_auto(
        instagram_golike_id_input=id_ins_gol,
        cookies_inp=cookie_inp,
        wait_time=wait,
        maxcount=tryJob,
        current_account=username,
        loop=loop
    )
    print(output)
    input(system_color("[.] Enter để đóng bỏ\n-> "))

if __name__ == "__main__":
    main()