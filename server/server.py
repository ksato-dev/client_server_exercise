from flask import Flask, request, jsonify, send_file
import os
import os

app = Flask(__name__)

# データベースや画像ファイルの仮のリスト
IMAGE_FILE_NAMES = [
    'apples/vertical_flip_Screen Shot 2018-06-07 at 2.57.05 PM.png',
    'apples/vertical_flip_Screen Shot 2018-06-08 at 5.21.06 PM.png'
]

@app.route('/check_connection', methods=['GET'])
def check_connection():
    return jsonify({
        'status': 'success',
        'message': 'Connection is fine.'
    })

@app.route('/get_image_file_names', methods=['GET'])
def get_image_file_names():
    return jsonify({
        'status': 'success',
        'file_path_list': IMAGE_FILE_NAMES
    })

@app.route('/image_data', methods=['POST'])
def image_data():
    data = request.get_json()
    image_path = data.get('image_path')

    if image_path in IMAGE_FILE_NAMES:
        # 画像ファイルが存在する場合、仮の画像ファイルを返す
        try:
            # 実際には適切なパスを指定する必要があります
            return send_file(image_path, mimetype='image/png')
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

@app.route('/another_endpoint', methods=['GET'])
def another_endpoint():
    return jsonify({
        'data': 'some_data',
        'status': 'success'
    })

@app.route('/save_annotations', methods=['POST'])
def save_annotations():
    data = request.get_json()
    image_path = data.get('image_path')

    if image_path in IMAGE_FILE_NAMES:
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

