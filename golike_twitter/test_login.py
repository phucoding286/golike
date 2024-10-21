import requests

headers = {
    "Host": "api.x.com",
    "Cookie": "guest_id=172947819920708533; night_mode=2; guest_id_marketing=v1%3A172947819920708533; guest_id_ads=v1%3A172947819920708533; personalization_id=\"v1_WxH6QogaYcDZeKO1/yUTnA==\"; gt=1848191643624902912; att=1-jZ5PmtUzzBdsIyacy1SOatMSSjabBWSpFaris9kA",
    "Content-Length": "287",
    "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"",
    "X-Twitter-Client-Language": "en",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua-Mobile": "?0",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36",
    "Content-Type": "application/json",
    "X-Client-Transaction-Id": "cS0Y1/wRfsRZu5BrUI5KcfLVepPGD6sCAq8PpQIE2WF/76yudaQcAhsILsEC68UEztQtt3MNYP+OtG6F0nSPNJafkyLrcg",
    "X-Guest-Token": "1848191643624902912",
    "X-Twitter-Active-User": "yes",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept": "*/*",
    "Origin": "https://x.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://x.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
  }

data = {
    "flow_token": "g;172947819920708533:-1729478508967:4FhDeUH2Yn8KXYthRr5nLxiK:1",
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

response = requests.post(
    url="https://api.x.com//1.1/onboarding/task.json",
    headers=headers,
    json=data
)

print(response.text)