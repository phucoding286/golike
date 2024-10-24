import requests
from golike_features import get_jobs, drop_job

r_get_jobs = get_jobs("720060")
print(r_get_jobs)
print(drop_job(r_get_jobs[1], r_get_jobs[3], "720060", r_get_jobs[2]))


# instagram headers
# headers = {
#         "authority": "www.instagram.com",
#         "method": "POST",
#         "path": "/graphql/query",
#         "scheme": "https",
#         "accept": "*/*",
#         "accept-language": "us",
#         "content-length": "1303",
#         "content-type": "application/x-www-form-urlencoded",
#         "cookie": "dpr=1.25; mid=Zw9CFgALAAFmS99R-xcNXquEREN_; datr=FkIPZ2qDjztFdLrsf2-XmWT7; ig_did=C23A3BE0-44BD-46E4-A360-F90379A9B886; ps_l=1; ps_n=1; wd=954x746; ds_user_id=69654070653; sessionid=69654070653%3ARpikM4ucMOmy0t%3A8%3AAYdHUum8ZkcjCOYnLuOrnpLPwkulfGNerppUdRY2FQ; csrftoken=qweTQnNCnD63aQC1UIIoddyJs2Uufu03; rur=\"HIL\\05469654070653\\0541761275362:01f77eb9ab7cc170993a84a1483f108b1b60459cdbf6fc1b1c7fa95be4f6caf572b64bab\"", # cookies instagram (add later)
#         "origin": "https://www.instagram.com",
#         "priority": "u=1, i",
#         "referer": "https://www.instagram.com/p/DBVQhLeTZ1b/",
#         "sec-ch-prefers-color-scheme": "dark",
#         "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
#         "sec-ch-ua-full-version-list": "\"Microsoft Edge\";v=\"129.0.2792.79\", \"Not=A?Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"129.0.6668.90\"",
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-model": "\"\"",
#         "sec-ch-ua-platform": "\"Windows\"",
#         "sec-ch-ua-platform-version": "\"8.0.0\"",
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "same-origin",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
#         "x-asbd-id": "129477",
#         "x-bloks-version-id": "d064162f4a1bc5cbc2a7ce44dd98b555613e0264ce1d0ebd6be60a79d3c58f44",
#         "x-csrftoken": "qweTQnNCnD63aQC1UIIoddyJs2Uufu03", # csrftoken (add later)
#         "x-fb-friendly-name": "PolarisAPIGetFrCookieQuery",
#         "x-fb-lsd": "gtE021O5IF-2TGA5JwktM8",
#         "x-ig-app-id": "936619743392459"
#     }

# comment_payloads = {
#   "av": 17841469741829738,
#   "__d": "www",
#   "__user": 0,
#   "__a": 1,
#   "__req": "o",
#   "__hs": "20020.HYP:instagram_web_pkg.2.1..0.1",
#   "dpr": 1,
#   "__ccg": "UNKNOWN",
#   "__rev": 1017616473,
#   "__s": "449ev4:z64fid:17cwqe",
#   "__hsi": 7429169421485569974,
#   "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0k24o1DU2_CwjE1xoswaq0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo31w9O1TwQzXwae4UaEW2G0AEco5G0zK5o4q3y1Sx-0lKq2-azqwt8d-2u2J0bS1LwTwKG1pg2fwxyo6O1FwlEcUed6goK2O4UrAwHxW1oCz8rwHwrE5SEymUhw",
#   "__csr": "hI4k54v24bs_ROOOfN2Xkz9P9R8hpd9nlkhbGKG9KXgkTiyAaG9pHGnBRKrVHzr-WBDehvDByayppqWgGFbx97ADUizXx1e8CBx2cxGiQm8LBKbm696USlamjy9pbV4u8gTyUW5kawAx65VoCEG00PWU06DK0wk0QC0pWqE0Jy16Ag6Kl0dS2K06481Li0du0a7wjUbUcE56qt6kk0Smfih8qwk14WODF1foG2Yw3lwwQD80Eeh07XDwZJw8u1hwdZ04qw0IFw0jCE0nfw",
#   "__comet_req": 7,
#   "fb_dtsg": "NAcNgv81HCPMAYUafv3LQgOoaM4B_gQ4JSICPda9sCXm_Y_jTB5hG6A:17864642926059691:1729738253",
#   "jazoest": 26058,
#   "lsd": "P1DhF0Zc6oFlwHpbizDoqr",
#   "__spin_r": 1017616473,
#   "__spin_b": "trunk",
#   "__spin_t": 1729738298,
#   "fb_api_caller_class": "RelayModern",
#   "fb_api_req_friendly_name": "PolarisPostCommentInputRevampedMutation",
#   "variables": "{\"connections\":[\"client:root:__PolarisPostComments__xdt_api__v1__media__media_id__comments__connection_connection(data:{},media_id:\\\"3482762535647419739\\\",sort_order:\\\"popular\\\")\"],\"request_data\":{\"comment_text\":\"cute quá 😲\"},\"media_id\":\"3482762535647419739\"}",
#   "server_timestamps": True,
#   "doc_id": 7980226328678944
# }

# r = requests.post(
#     url="https://www.instagram.com/graphql/query",
#     headers=headers,
#     data=comment_payloads
# )

# print(r.text)