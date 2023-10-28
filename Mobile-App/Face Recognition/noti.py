import requests
data = {
    "app_id": "0a807065-20b8-4c43-a875-50bc94fd049f",
    "included_segments": ["All"],
    "headings" : {"en": "Alert"},
    "contents": {"en": "Unknown Person detected!"},
    "big_picture" : "https://i.pinimg.com/736x/e2/d4/93/e2d493626c1870189e250b551434d218.jpg"
}


requests.post(
    "https://onesignal.com/api/v1/notifications",
    headers={"Authorization": "Basic MzdmZjNmZDYtNmIxZC00M2E4LTkxMjctZThkMjA3ODRkZjg1"},
    json=data
)