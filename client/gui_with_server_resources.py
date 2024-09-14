import streamlit as st
import os
import cv2

from http_requests import *

# Server URL
ROOT_URL = 'http://34.69.26.68:5000/'

# セッション状態の初期化
if 'image_index' not in st.session_state:
    st.session_state['image_index'] = 0

if 'image_paths' not in st.session_state:
    st.session_state['image_paths'] = []

if 'save_results' not in st.session_state:
    st.session_state['save_results'] = {}

if 'load_state' not in st.session_state:
    st.session_state['load_state'] = 'initial'

if 'folder_name' not in st.session_state:
    st.session_state['folder_name'] = None


# 画像フォルダの読み込み関数
def load_images(folder_name):
    if not folder_name:
        st.warning('画像フォルダ名を入力してください。')
    else:
        # サーバーから画像ファイル名のリストを取得
        # st.session_state['image_paths'] = request_get_image_file_names(ROOT_URL, folder_name)
        response_json = request_get_image_file_names(ROOT_URL, folder_name)
        st.session_state['image_paths'] = response_json['file_path_list']
        if not st.session_state['image_paths']:
            st.warning('画像が見つかりませんでした。')
        else:
            st.session_state['image_index'] = 0
            st.session_state['save_results'] = {}
            # save_resultsを初期化
            # print(response_json['save_results'])
            if not any(response_json['save_results']):
            # if True:
                for img_id, img_path in enumerate(st.session_state['image_paths']):
                    st.session_state['save_results'][img_id] = [img_path, 'Unknown']
            else:
                # print("any")
                # print("=====")
                for img_id in response_json['save_results'].keys():
                    st.session_state['save_results'][int(img_id)] = response_json['save_results'][img_id]
            st.success('画像を読み込みました')
            st.session_state['load_state'] = 'loaded'

# 次の画像へ進む関数
def next_image():
    st.session_state['image_index'] = (st.session_state['image_index'] + 1) % len(st.session_state['image_paths'])

# 前の画像に戻る関数
def prev_image():
    st.session_state['image_index'] = (st.session_state['image_index'] - 1) % len(st.session_state['image_paths'])

# ラベルを保存する関数
def save_labels():
    # サーバーにアノテーションを保存
    request_save_annotations(ROOT_URL, st.session_state['save_results'], st.session_state['folder_name'])
    st.success('ラベルを保存しました')

# ラベルが変更されたときの処理
def update_label():
    # 現在の画像IDとパスを取得
    curr_img_id = st.session_state['image_index']
    current_image_path = st.session_state['image_paths'][curr_img_id]
    # ラベル用のキーを取得
    label_key = f"label_{current_image_path}"
    # 現在のラベルを取得
    label = st.session_state[label_key]
    # save_resultsを更新
    st.session_state['save_results'][curr_img_id] = [current_image_path, label]

# 「読み込み」ボタンを押したときの処理
if st.button('読み込み'):
    st.session_state['load_state'] = 'waiting_for_input'

# 読み込み状態に応じた処理
if st.session_state['load_state'] == 'waiting_for_input':
    st.session_state['folder_name'] = st.text_input('フォルダ名を入力してください', key='folder_input')
    if st.button('フォルダを読み込む'):
        load_images(st.session_state['folder_name'])

# 画像が読み込まれている場合
if st.session_state['load_state'] == 'loaded' and st.session_state['image_paths']:
    # レイアウトの設定
    left_col, right_col = st.columns([1, 3])

    with left_col:
        img_path_list = st.session_state['image_paths']
        curr_img_id = st.session_state['image_index']
        current_image_path = st.session_state['image_paths'][curr_img_id]

        st.write(f'現在の画像 ID: {curr_img_id + 1} / {len(img_path_list)}')

        # ラベルの選択肢を定義
        label_options = ['Unknown', 'Fresh', 'Stale']

        # ラベル用のキーを定義
        label_key = f"label_{current_image_path}"

        # ラベルの初期値を設定
        if curr_img_id in st.session_state['save_results']:
            # save_resultsからラベルを取得
            label = st.session_state['save_results'][curr_img_id][1]
            if label_key not in st.session_state:
                st.session_state[label_key] = label
        else:
            # デフォルトのラベルを設定
            if label_key not in st.session_state:
                st.session_state[label_key] = 'Unknown'

        # ラベルの選択
        label = st.radio(
            'ラベルを選択してください',
            label_options,
            key=label_key,
            on_change=update_label
        )

        # ボタンの配置
        st.button('前の画像に戻る', on_click=prev_image)
        st.button('次の画像へ進む', on_click=next_image)
        st.button('サーバーに保存', on_click=save_labels)

    with right_col:
        img = request_image_data(ROOT_URL, current_image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, use_column_width=True)
else:
    st.write('「読み込み」ボタンを押して画像を読み込んでください。')
