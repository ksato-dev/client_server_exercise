import requests
import json

url = 'http://34.69.26.68:5000/image_data'
data = {
    'image_path': 'apples/vertical_flip_Screen Shot 2018-06-07 at 2.57.05 PM.png'
}

# POST リクエストを送信
response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

# レスポンスの確認
if response.status_code == 200:
    response_json = response.json()
    if response_json['status'] == 'success':
        print("Image data retrieved successfully.")
    else:
        print("Error:", response_json['message'])
else:
    print(f"Failed to retrieve image data. Status code: {response.status_code}")
