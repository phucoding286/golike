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
  "content-length": "316",
  "content-type": "application/x-www-form-urlencoded",
  "cookie": "guest_id=v1%3A172941924723497213; night_mode=2; guest_id_marketing=v1%3A172941924723497213; guest_id_ads=v1%3A172941924723497213; kdt=qyzl9KOMcPUvC0o2LQwzEpBqohEncPnqKCNhpLLl; auth_token=56a9eb1b6bdc5c3bad09bd7decdedf5b13977ca3; ct0=9847771b6e383c7fd89262e72a8b4c2e1247f22977f994b9e132fede367d8716a44d34dbc55dd8fd338db092b98d1b9d84b8efd02589b0e8c928b5d3ab302850c03131ba7e1601bab227e3f37cda18dd; twid=u%3D1847945033854722048; personalization_id=\"v1_nIr/uIHJ/pzR4oP7tYwdHg==\"; external_referer=padhuUp37zhD6%2F29CpQtyhGQCUl05AFo|0|8e8t2xd8A2w%3D; lang=en",
  "origin": "https://x.com",
  "priority": "u=1, i",
  "referer": "https://x.com/ngocquyen2704",
  "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
  "x-client-transaction-id": "7577jrFfEdY29QBxg7pUruGCzvisRZYPnO1HSRv7gJ+qcUYFnTcrYZwmN5sqR6fLSTm5Ke31a3pcvQ0h696JvVdLUAkh7A",
  "x-client-uuid": "cfca0c29-831a-4039-b664-edaf45cbd7ee",
  "x-csrf-token": "9847771b6e383c7fd89262e72a8b4c2e1247f22977f994b9e132fede367d8716a44d34dbc55dd8fd338db092b98d1b9d84b8efd02589b0e8c928b5d3ab302850c03131ba7e1601bab227e3f37cda18dd",
  "x-twitter-active-user": "yes",
  "x-twitter-auth-type": "OAuth2Session",
  "x-twitter-client-language": "en"
}

data = {
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
  "user_id": 741910485038075904
}


response = requests.post(
    url="https://x.com/i/api/1.1/friendships/create.json",
    headers=headers,
    data=data
)

print(response.status_code, response.text)