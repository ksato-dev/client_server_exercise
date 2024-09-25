from flask import Flask, request, jsonify, send_file
import os
import glob
import cv2
# import io
import base64
import json
import pathlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# データベースや画像ファイルの仮のリスト
# IMAGE_FILE_NAMES = [
#     'apples/vertical_flip_Screen Shot 2018-06-07 at 2.57.05 PM.png',
#     'apples/vertical_flip_Screen Shot 2018-06-08 at 5.21.06 PM.png'
# ]
# IMAGE_FILE_NAMES = glob.glob('apples/*.png')
IMAGE_FILE_NAMES = []
CURR_FOLDER_NAME = ""


@app.route('/check_connection', methods=['GET'])
def check_connection():
    return jsonify({
        'status': 'success',
        'message': 'Connection is fine.'
    })

@app.route('/get_image_file_names', methods=['POST'])
def get_image_file_names():
    data = request.get_json()
    folder_name = data.get('folder_name')
    global CURR_FOLDER_NAME
    CURR_FOLDER_NAME = folder_name
    global IMAGE_FILE_NAMES
    # IMAGE_FILE_NAMES = glob.glob(f'{folder_name}/*.*')
    IMAGE_FILE_NAMES = [pathlib.Path(elem).name for elem in glob.glob(f'{folder_name}/*.png')]
    IMAGE_FILE_NAMES += [pathlib.Path(elem).name for elem in glob.glob(f'{folder_name}/*.jpg')]
    IMAGE_FILE_NAMES += [pathlib.Path(elem).name for elem in glob.glob(f'{folder_name}/*.jpeg')]
    # print(IMAGE_FILE_NAMES)

    label_dict = {}
    label_dict['save_results'] = {}
    if os.path.exists(f'{folder_name}/label.json'):
        with open(f'{folder_name}/label.json', mode='r') as f:
            label_dict = json.load(f)

    return jsonify({
        'status': 'success',
        'save_results': label_dict['save_results'],
        'file_path_list': IMAGE_FILE_NAMES
    })

@app.route('/image_data', methods=['POST'])
def image_data():
    data = request.get_json()
    image_path = data.get('image_path')
    print(image_path)
    tgt_image_path = os.path.join(CURR_FOLDER_NAME, image_path)
    print(tgt_image_path)

    global IMAGE_FILE_NAMES
    # print(IMAGE_FILE_NAMES)
    if image_path in IMAGE_FILE_NAMES:
        # 画像ファイルが存在する場合、仮の画像ファイルを返す
        try:
            print("hoge")
            if not os.path.exists(tgt_image_path):
                response = {
                    'message': f'{tgt_image_path} not exists.',
                    'status': 'error'
                }
                return jsonify(response)
            else:
                print("piyo")
                image = cv2.imread(tgt_image_path)

                # 画像を JPEG 形式でエンコード
                is_success, buffer = cv2.imencode(".png", image)
                print(is_success)

                if not is_success:
                    return jsonify({'status': 'error', 'message': 'Failed to encode image'}), 500

                # エンコードされたバイナリデータをバイナリストリームに変換
                # image_bytes = io.BytesIO(buffer)
                image_bytes = base64.b64encode(buffer).decode('utf-8')
                # print(image_bytes)

                response = {
                    'image_bytes': image_bytes,
                    'status': 'success'
                }
                return jsonify(response)
                # レスポンスとして画像データを返す
                # return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name='image.png')
                # return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name='image.png')
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': 'Image not found.'
        })

@app.route('/save_annotations', methods=['POST'])
def save_annotations():
    data = request.get_json()
    # print(data)
    folder_name = data.get('folder_name')

    with open(f'{folder_name}/label.json', mode='w') as f:
        json.dump(data, f, indent=2)

    # if image_path in IMAGE_FILE_NAMES:
    if True:
        # Annotation 保存処理をここに実装する必要があります
        return jsonify({
            'status': 'success'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Image not found.'
        })

if __name__ == '__main__':
    # アプリケーションをデバッグモードで実行
    app.run(debug=True, host='0.0.0.0', port=5000)

