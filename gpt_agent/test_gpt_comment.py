import requests

url = "http://127.0.0.1:5001/generate-comment"


data = {
    "menu_name": "고소한 귀리죽",
    "ingredients": ["귀리", "아몬드", "호두"],
    "nutrients": {
        "protein": 7,
        "fat": 4,
        "carbohydrate": 20
    }
}

res = requests.post(url, json=data)

print("응답 코드:", res.status_code)
print("생성된 코멘트:")
print(res.json())
