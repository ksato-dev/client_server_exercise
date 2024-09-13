import requests

url = 'http://34.69.26.68:5000/get_image_file_names'

# GET リクエストを送信
response = requests.get(url)

# レスポンスの確認
if response.status_code == 200:
    print("Response JSON:", response.json())
else:
    print(f"Failed to get image file names. Status code: {response.status_code}")
