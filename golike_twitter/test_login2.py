import requests

response = requests.get("https://x.com/i/flow/login")
print(response.headers)
# cookies = response.cookies
# cookie_string = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
# response = requests.post("https://api.x.com/1.1/jot/client_event.json", headers={"cookies": cookie_string})
# print(response.text)