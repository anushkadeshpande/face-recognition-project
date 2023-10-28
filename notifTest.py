import requests
data = {
    "app_id": "0a807065-20b8-4c43-a875-50bc94fd049f",
    "included_segments": ["All"],
    "headings" : {"en": "Alert"},
    "contents": {"en": "Unknown Person detected!"},
    "big_picture" : "https://upload.wikimedia.org/wikipedia/commons/9/98/V_x_Samsung_Galaxy_August_2021.png"
}


requests.post(
    "https://onesignal.com/api/v1/notifications",
    headers={"Authorization": "Basic MzdmZjNmZDYtNmIxZC00M2E4LTkxMjctZThkMjA3ODRkZjg1"},
    json=data
)