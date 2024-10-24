from colorama import Fore, Style
import time
import colorama
from test_login import login_twitter
from test_get_job_golike import check_tw_account_id, get_jobs, drop_job, verify_complete_job
from test_follow import tw_follow
colorama.init()

def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(Fore.YELLOW + f"\r{i}s " + Style.RESET_ALL, end="")
        print(Fore.BLUE + text + Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0

id_golike_tw, username_golike_tw = check_tw_account_id()[0]
x_csrf_token, cookie = login_twitter(username_golike_tw, "7vnrzkseven")

while True:
    r_get_job = get_jobs(id_golike_tw)
    print(r_get_job)

    if "error" in r_get_job:
        print("đã có lỗi khi nhận job, bỏ qua")
        waiting_ui(60, "đợi 60s để tiếp tục")
        continue
    else:
        print("nhận job thành công")

        
    if r_get_job[2] != "follow":
        print("job khác follow nên bỏ")
        print(drop_job(r_get_job[1], r_get_job[3], id_golike_tw))
        waiting_ui(5, "đợi 5s để tiếp tục")
        continue

    target_link = r_get_job[0]
    follow_output = tw_follow(cookie, x_csrf_token, r_get_job[3], target_link)

    if "following" not in follow_output:
        print(follow_output)
        print("đã có lỗi khi follow")
        print(drop_job(r_get_job[1], r_get_job[3], id_golike_tw))
        waiting_ui(60, "đợi 60s để tiếp tục")
        continue
    
    print(follow_output)
    waiting_ui(10, "đợi 10s để xác minh job")
    
    vrf_output = verify_complete_job(r_get_job[1], id_golike_tw)
    if "error" in vrf_output:
        print("đã có lỗi khi xác minh job")
        print(drop_job(r_get_job[1], r_get_job[3], id_golike_tw))
        waiting_ui(60, "đợi 60s để tiếp tục")
        continue
    else:
        print("xác minh job thành công")
        print(vrf_output)
        waiting_ui(60, "đợi 60s để tiếp tục")