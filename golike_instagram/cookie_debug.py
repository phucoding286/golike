from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import os, shutil, json

ua = json.load(open("./ua.json"))['UA']
if str(ua) == '[]':
    input("[!] vui lòng thêm user agent")

def __i(driver_name="edge"):
    if driver_name == "edge":
        try:
            return driver_name, EdgeChromiumDriverManager().install()
        except:
            return driver_name, "error"
    elif driver_name == "chrome":
        try:
            return driver_name, ChromeDriverManager().install()
        except:
            return driver_name, "error"
    
try: driver_name, res = __i('edge')
except: driver_name, res = __i('chrome')
print(f"[*] đường dẫn edge driver của bạn -> {res}")

options = webdriver.EdgeOptions() if driver_name == "edge" else webdriver.ChromeOptions()
shutil.rmtree(os.path.abspath("./golike")+"\\user_data") if os.path.exists(os.path.abspath("./golike")+"\\user_data") else 0
options.add_argument("--user-data-dir="+os.path.abspath("./golike")+"\\user_data")
options.add_argument("--log-level=3")
options.add_argument(f"--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)")

driver = webdriver.Edge(options=options) if driver_name == "edge" else webdriver.Chrome()
driver.get("https://www.instagram.com")

cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in input("[?] nhập cookies\n-> ").split('; ')}
for name, value in cookies.items():
    driver.add_cookie({'name': name, 'value': value, 'path': '/', 'domain': '.instagram.com'})

driver.refresh()
input("[*] enter để đóng\n-> ")
print("[#] đang đóng chromium...")
driver.quit()