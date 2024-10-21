import requests
import json

url = "https://api.x.com/1.1/onboarding/task.json"
headers = {
    "Cookie": "guest_id=172947819920708533; night_mode=2; guest_id_marketing=v1%3A172947819920708533; guest_id_ads=v1%3A172947819920708533; gt=1848345074910028086; att=1-ekyZDoU5fJ8QNIy1DuV90xuu737XEQHRJqoFyvrL; personalization_id=\"v1_qFFHqBBeb84CTmlNh493xQ==\"",
    "Sec-Ch-Ua": '"Not;A=Brand";v="24", "Chromium";v="128"',
    "X-Twitter-Client-Language": "en",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua-Mobile": "?0",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
    "Content-Type": "application/json",
    "X-Client-Transaction-Id": "ps8TtcU0v3PV+icx7R59S5oVdnfynR2RpUx6uWmmSITPK/Uj8liewbGXObSTorSwujBIYKTqN8qb2tSaWWQHrG7z/+bBpQ",
    "X-Guest-Token": "1848345074910028086",
    "X-Twitter-Active-User": "yes",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept": "*/*",
    "Origin": "https://x.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://x.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
}

payload = {
    "flow_token": "g;172947819920708533:-1729515325535:0DfwpS7rs3z0q18JDuhjO5bP:1",
    "subtask_inputs": [
        {
            "subtask_id": "LoginEnterUserIdentifierSSO",
            "settings_list": {
                "setting_responses": [
                    {
                        "key": "user_identifier",
                        "response_data": {
                            "text_data": {
                                "result": "kiemtienon63911"
                            }
                        }
                    }
                ],
                "link": "next_link"
            }
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
print(response.text)