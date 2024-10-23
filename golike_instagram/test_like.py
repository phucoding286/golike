from instagram_interection import like_instagram
from golike_features import get_jobs, drop_job

r_get_jobs = get_jobs("716983")
print(r_get_jobs)
print(drop_job(r_get_jobs[1], r_get_jobs[3], "716983", r_get_jobs[2]))

# cookie = "dpr=1.25; mid=Zw9CFgALAAFmS99R-xcNXquEREN_; datr=FkIPZ2qDjztFdLrsf2-XmWT7; ig_did=C23A3BE0-44BD-46E4-A360-F90379A9B886; ps_l=1; ps_n=1; ds_user_id=69480847920; sessionid=69480847920%3AhYyDbPArcjwLTC%3A21%3AAYf-kuyPw5QhJm_nA2F8Tf174GVT-pQ2dt2t9eoATw; csrftoken=ZFiXWz2ya0XSoYhZQi0Rs1QMdFFvqUWO; wd=954x746; rur=\"CCO\\05469480847920\\0541761230632:01f7b25acc604c791f1e6d95cd0e7376c7d10ddf419e048ae46fc91f71b457442ef4afa6\""
# insta_link = "https://www.instagram.com/p/DBVQhLeTZ1b/"
# object_id = "3468480231705879903"
# proxy = True
# task_type = "like"

# print(like_instagram(cookies=cookie, insta_link=insta_link, object_id=object_id, proxy=proxy))