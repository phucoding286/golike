from login_instagram import __login
import colorama
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

def lg_get_ck():
    username = input(system_color("[?] Nhập username instagram\n-> "))
    password = input(system_color("[?] Nhập vào password instagram\n-> "))

    output = __login(username, password, None)
    if "success" in output:
        print(success_color(output['success']))
        print(success_color(f"[!] Đây là cookie của bạn\n-> {output['cookies']}"))
    else:
        print(error_color(output['error']))
    input(system_color("[*] Enter để quay lại\n-> "))

if __name__ == "__main__":
    lg_get_ck()