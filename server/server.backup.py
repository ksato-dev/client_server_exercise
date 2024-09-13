from flask import Flask, request, jsonify, send_file
import cv2
import os
import numpy as np
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/image_data', methods=['POST'])
def receive_message():
    data = request.get_json()  # JSONリクエストボディを取得
    image_path = 'apples/' + data.get('image_path', 'No message provided')

    if not os.path.exists(image_path):
        response = {
            'message': f'{image_path} not exists.',
            'status': 'error'
        }
        return jsonify(response)
    else:
        image = cv2.imread(image_path)

        # 画像を JPEG 形式でエンコード
        is_success, buffer = cv2.imencode(".png", image)

        if not is_success:
            return jsonify({'status': 'error', 'message': 'Failed to encode image'}), 500

        # エンコードされたバイナリデータをバイナリストリームに変換
        image_bytes = io.BytesIO(buffer)

        response = {
            'image_bytes': image_bytes,
            'status': 'success'
        }
        # レスポンスとして画像データを返す
        return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name='image.png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
