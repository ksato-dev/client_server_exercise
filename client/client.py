import requests
import cv2
import numpy as np
import io
import json

# POST リクエストを送信する URL
url = 'http://34.69.26.68:5000/image_data'

# POST リクエストに含めるデータ（JSON形式）
data = {
    'image_path': 'vertical_flip_Screen Shot 2018-06-07 at 3.00.46 PM.png'
}

# HTTP POST リクエストを送信
response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

# レスポンスのステータスコードを確認
if response.status_code == 200:
    # レスポンスのバイナリデータを取得
    image_data = response.content
    
    # バイナリデータを NumPy 配列に変換
    nparr = np.frombuffer(image_data, np.uint8)
    
    # NumPy 配列を画像にデコード
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is not None:
        # 画像をファイルとして保存
        cv2.imwrite('output_image.png', image)
        print("Image saved successfully as 'output_image.png'")
    else:
        print("Failed to decode image")
else:
    print(f"Failed to retrieve image. Status code: {response.status_code}")
