import requests
import json

url = 'http://34.69.26.68:5000/save_annotations'
data = {
    'image_path': 'apples/vertical_flip_Screen Shot 2018-06-07 at 2.57.05 PM.png'
}

# POST リクエストを送信
response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

# レスポンスの確認
if response.status_code == 200:
    response_json = response.json()
    if response_json['status'] == 'success':
        print("Annotation saved successfully.")
    else:
        print("Error:", response_json.get('message', 'Unknown error'))
else:
    print(f"Failed to save annotation. Status code: {response.status_code}")
