import requests

headers = {
  "authority": "api.twitter.com",
  "method": "POST",
  "path": "/1.1/onboarding/task.json?flow_name=login",
  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "vi",
  "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
  "content-length": "930",
  "content-type": "application/json",
  "cookie": "", # add later in code
  "origin": "https://twitter.com",
  "priority": "u=1, i",
  "referer": "https://twitter.com/",
  "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-site",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
  "x-client-transaction-id": "RzbFRPaMDR+IPONaBuOeMJBLIyUChfRxAC3w8MmgZ/IX31ItIbCThaQoReE/37eqLrKDgEX9BnRplJXkV+0/uCd3t+MNRA",
  "x-guest-token": "1849048881352556934",
  "x-twitter-active-user": "yes",
  "x-twitter-client-language": "vi"
}

follow_payloads = {
  "include_profile_interstitial_type": 1,
  "include_blocking": 1,
  "include_blocked_by": 1,
  "include_followed_by": 1,
  "include_want_retweets": 1,
  "include_mute_edge": 1,
  "include_can_dm": 1,
  "include_can_media_tag": 1,
  "include_ext_is_blue_verified": 1,
  "include_ext_verified_type": 1,
  "include_ext_profile_image_shape": 1,
  "skip_status": 1,
  "user_id": 109065990
}

url = "https://x.com/i/api/1.1/friendships/create.json"

def tw_follow(target_id: int):
    # headers['cookie'] = cookie
    follow_payloads['user_id'] = target_id
    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=follow_payloads
        )
        return response.status_code, response.text
    except:
        return "đã có lỗi"
    

from test_login2 import login_twitter

headers = login_twitter("kiemtienon63911", "7vnrzkseven")
print(tw_follow(25073877))