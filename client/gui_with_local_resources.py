import streamlit as st
import os
import cv2

# セッション状態の初期化
if 'image_index' not in st.session_state:
    st.session_state['image_index'] = 0

if 'image_paths' not in st.session_state:
    st.session_state['image_paths'] = []

if 'save_results' not in st.session_state:
    st.session_state['save_results'] = {}

# 画像フォルダのパスを設定（必要に応じて変更してください）
image_folder = 'C:\\Users\\sksof\\Downloads\\archive\\apples'  # 例: 'images'

# 画像フォルダの読み込み関数
def load_images():
    if not image_folder:
        st.warning('画像フォルダのパスを入力してください。')
    elif os.path.exists(image_folder):
        st.session_state['image_paths'] = [
            os.path.join(image_folder, f)
            for f in os.listdir(image_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]
        if not st.session_state['image_paths']:
            st.warning('画像が見つかりませんでした。')
        else:
            st.session_state['image_index'] = 0
            st.session_state['save_results'] = {}
            st.success('画像を読み込みました')
    else:
        st.error('指定したフォルダが存在しません')

# 次の画像へ進む関数
def next_image():
    st.session_state['image_index'] = (st.session_state['image_index'] + 1) % len(st.session_state['image_paths'])

# 前の画像に戻る関数
def prev_image():
    st.session_state['image_index'] = (st.session_state['image_index'] - 1) % len(st.session_state['image_paths'])

# ラベルを保存する関数
def save_labels():
    with open('labels.txt', 'w', encoding='utf-8') as f:
        for id, (img_path, label) in st.session_state['save_results'].items():
            f.write(f'{os.path.basename(img_path)}\t{label}\n')
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

# 画像フォルダの読み込み
if st.button('読み込み', on_click=load_images):
    pass  # on_clickで処理を行うため、ここでは何もしない

# 画像が読み込まれている場合
if st.session_state['image_paths']:
    # レイアウトの設定
    left_col, right_col = st.columns([1, 3])

    with left_col:
        img_path_list = st.session_state['image_paths']
        curr_img_id = st.session_state['image_index']
        current_image_path = st.session_state['image_paths'][curr_img_id]

        st.write(f'現在の画像 ID: {curr_img_id + 1} / {len(img_path_list)}')

        # ラベルの選択肢を定義
        label_options = ['ラベル１', 'ラベル２', 'ラベル３']

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
                st.session_state[label_key] = 'ラベル１'

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
        st.button('保存', on_click=save_labels)

    with right_col:
        img = cv2.imread(current_image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, use_column_width=True)
else:
    st.write('「読み込み」ボタンを押して画像を読み込んでください。')
