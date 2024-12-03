from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
import requests
import random
import os
import shutil
import colorama
import time
colorama.init()

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

def captcha_dectect(cookie_str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "authority": "www.instagram.com",
        "method": "GET",
        "path": "/",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "vi",
        "cache-control": "max-age=0",
        "cookie": cookie_str,
        "dpr": "1.25",
        "priority": "u=0, i",
        "referer": "https://www.instagram.com/accounts/onetap/?next=%2F",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"8.0.0\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "viewport-width": "954"
    }
    r = requests.get("https://instagram.com/", headers=headers)
    return True if len(r.text.split("https://www.instagram.com/challenge/?next=")) > 1 else False

class PassInstagramCaptcha():
    def __init__(self, cookie_str, huggingfaces_keys=[]):
        self.driver_install()
        self.driver = self.__driver_i()
        self.add_instagram_cookie(cookie_str)

        self.cookie_str = cookie_str
        self.huggingfaces_openai_url = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
        
        if str(huggingfaces_keys) == "[]":
            self.huggingfaces_keys = {"Authorization": "Bearer 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"}
        else:
            self.huggingfaces_keys = {"Authorization": random.choice(huggingfaces_keys)}
    
    def driver_install(self):
        install_output = ChromeDriverManager().install()
        print(system_color(f"[*] Đường dẫn driver đã tải\n-> {install_output}"))

    def __driver_i(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--log-level=3")
        options.add_argument("--headless=old")
        options.add_argument(f"user-data-dir=./driver_data")
        
        if os.path.exists("./driver_data"):
            shutil.rmtree("./driver_data")

        driver = webdriver.Chrome(
            options=options,
            keep_alive=True
        )
        return driver

    def add_instagram_cookie(self, cookie_str):
        self.driver.get("https://instagram.com/")
        cookie = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookie_str.split('; ')}
        for name, value in cookie.items():
            self.driver.add_cookie({'name': name, 'value': value, 'path': '/', 'domain': '.instagram.com'})
        self.driver.refresh()

    def __click_to_checkbox(self):
        captcha_iframe1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "recaptcha-iframe"))
        )
        self.driver.switch_to.frame(captcha_iframe1)

        captcha_iframe2 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']"))
        )
        self.driver.switch_to.frame(captcha_iframe2)

        captcha_checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-anchor"]'))
        )
        captcha_checkbox.click()
        return captcha_iframe1
    
    def __click_to_audio_captcha(self, captcha_iframe1):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(captcha_iframe1)

        captcha_iframe3 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']"))
        )
        self.driver.switch_to.frame(captcha_iframe3)

        audio_captcha_type = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='button-holder audio-button-holder']"))
        )
        audio_captcha_type.click()

    def __processing_captcha(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="PLAY"]'))
        )
        button.click()

        get_audio_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//audio[@id='audio-source']"))
        )

        audio_link = get_audio_link.get_attribute("src")
        r = requests.get(audio_link)
        
        content_ex = None
        for _ in range(5):
            try:
                r = requests.post(
                self.huggingfaces_openai_url,
                headers=self.huggingfaces_keys,
                data=r.content
                )
                content_ex = r.json()['text']
                break
            except:
                print(r.text)
                print(error_color("[!] Error đã có lỗi khi yêu cầu giải, thử lại..."))
                continue
        if content_ex is None:
            raise ValueError("Lỗi api giải captcha")
        
        send_ex = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='audio-response']"))
        )
        send_ex.send_keys(content_ex)

        verify_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='recaptcha-verify-button']"))
        )
        verify_btn.click()

    def captcha_auto_detecting_and_process(self):
        if captcha_dectect(self.cookie_str):
            print(system_color("[!] Đã phát hiện captcha! tiến hành giải captcha..."))
            try:
                iframe1 = self.__click_to_checkbox()
                self.__click_to_audio_captcha(iframe1)
                self.__processing_captcha()
                
                self.driver.switch_to.default_content()
                next_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and text()="Next"]'))
                )
                next_btn.click()
                
                time.sleep(10)
                self.driver.quit()
                return {"captcha_detect": True, "success": "Giải captcha thành công!"}
            except:
                self.driver.quit()
                return {"captcha_detect": True, "error": "Đã có lỗi khi giải captcha"}
        else:
            self.driver.quit()
            print(system_color("Không phát hiện captcha!"))
            return {"captcha_detect": False}