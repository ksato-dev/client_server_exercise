from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    response = {
        'message': "Hello, World",
        'status': 'success'
    }
    return jsonify(response)

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()  # JSONリクエストボディを取得
    message = data.get('message', 'No message provided')
    response = {
        'received_message': message,
        'status': 'success'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
