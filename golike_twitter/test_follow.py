import requests

headers = {
  "authority": "x.com",
  "method": "POST",
  "path": "/i/api/1.1/friendships/create.json",
  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
  "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
  "content-length": "306",
  "content-type": "application/x-www-form-urlencoded",
  "cookie": "", # add later in code
  "origin": "https://x.com",
  "priority": "u=1, i",
  "referer": "", # add later in code
  "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
  "x-client-transaction-id": "jRl287bDW1N1cOL7VOPwmTzLNkcHHFYbPXKOdvzkA34aSgphBzhK0HFgpo/Rs7H7g1IARI9GSNJraXTqmZ5D0LskCjS9jg",
  "x-client-uuid": "cfca0c29-831a-4039-b664-edaf45cbd7ee",
  "x-csrf-token": "", # add later in code
  "x-twitter-active-user": "yes",
  "x-twitter-auth-type": "OAuth2Session",
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
  "user_id": "" # add later in code
}

url = "https://x.com/i/api/1.1/friendships/create.json"

def tw_follow(cookie: str, x_csrf_token: str, target_id: int, target_link: str):
    headers['cookie'] = cookie
    headers['x-csrf-token'] = x_csrf_token
    follow_payloads['user_id'] = target_id
    headers['referer'] = target_link

    response = requests.post(
            url=url,
            headers=headers,
            data=follow_payloads
        )
    return response.status_code, response.text
    

from test_login import login_twitter

x_csrf_token, cookie = login_twitter("kiemtienon63911", "")
target_link = "https://x.com/realDonaldTrump"
print(tw_follow(cookie, x_csrf_token, 25073877, target_link))