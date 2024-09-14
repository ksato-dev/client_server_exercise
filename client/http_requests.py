import requests
import cv2
import numpy as np
import io
import json


def request_check_coonection(root_url: str):
    url = root_url + '/check_connection'

    # GET リクエストを送信
    response = requests.get(url)

    # レスポンスの確認
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print(f"Failed to check connection. Status code: {response.status_code}")


def request_image_data(root_url: str, tgt_img_path: str):
    # POST リクエストを送信する URL
    url = root_url + '/image_data'

    # POST リクエストに含めるデータ（JSON形式）
    # data = {
    #     'image_path': 'apples/vertical_flip_Screen Shot 2018-06-07 at 3.00.46 PM.png'
    # }
    data = {
        'image_path': tgt_img_path
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
        server_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if server_img is not None:
            # 画像をファイルとして保存
            # cv2.imwrite('output_image.png', image)
            print(response)
            return server_img
            # print("Image saved successfully as 'output_image.png'")
        else:
            print("Failed to decode image")
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")


def request_get_image_file_names(root_url: str, folder_name: str):
    url = root_url + '/get_image_file_names'

    data = {
        "folder_name": folder_name
    }
    # POST リクエストを送信
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

    # レスポンスの確認
    if response.status_code == 200:
        # print("Response JSON:", response.json())
        # return response.json()['file_path_list']
        return response.json()
    else:
        print(f"Failed to get image file names. Status code: {response.status_code}")


def request_save_annotations(root_url: str, save_results: dict, folder_name: str):
    url = root_url + '/save_annotations'
    # data = {
    #     'image_path': 'apples/vertical_flip_Screen Shot 2018-06-07 at 2.57.05 PM.png'
    # }
    data = {
        'save_results': save_results,
        "folder_name": folder_name
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
