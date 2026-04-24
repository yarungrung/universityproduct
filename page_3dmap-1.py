import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(layout="wide") # 讓地圖寬一點比較好看
st.title("北北基桃交通權衡值 3D 視覺化")

# --- 1. 讀取資料 ---
# 這裡使用 os 確保路徑正確
current_dir = os.path.dirname(os.path.abspath(__file__))
# 根據您上傳的檔名，請確保這裡是正確的 (csv 或 xlsx)
file_path = os.path.join(current_dir, '3D出圖data.csv')

try:
    # 讀取 CSV (如果是 Excel 請改用 pd.read_excel)
    df = pd.read_csv(file_path)
    
    # 確保資料沒問題 (檢查欄位名)
    # df 欄位應該包含：'終點經度', '終點緯度', '權衡值_TSC'
    
    # 稍微清理一下資料，確保數值正確
    df['權衡值_TSC'] = pd.to_numeric(df['權衡值_TSC'], errors='coerce').fillna(0)
    df['終點經度'] = pd.to_numeric(df['終點經度'], errors='coerce')
    df['終點緯度'] = pd.to_numeric(df['終點緯度'], errors='coerce')
    df = df.dropna(subset=['終點經度', '終點緯度'])

    # --- 2. 設定 Pydeck 圖層 (ColumnLayer) ---
    # 使用 ColumnLayer 最適合呈現「特定座標點」的高度
    layer = pdk.Layer(
        'ColumnLayer',
        data=df,
        get_position='[終點經度, 終點緯度]',
        get_elevation='權衡值_TSC',
        radius=200,          # 柱子的粗細
        elevation_scale=1,   # 高度縮放倍率 (如果柱子太矮可以調大)
        elevation_range=[0, 5000],
        get_fill_color='[200, 30, 0, 160]', # 顏色 [R, G, B, 透明度]
        pickable=True,
        extruded=True,
    )

    # --- 3. 設定攝影機視角 ---
    # 以資料的平均中心點作為視角中心
    view_state = pdk.ViewState(
        latitude=df['終點緯度'].mean(),
        longitude=df['終點經度'].mean(),
        zoom=10,
        pitch=45,
    )

    # --- 4. 顯示地圖 ---
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>地點:</b> {終點}<br/><b>交通方式:</b> {交通方式}<br/><b>TSC 權衡值:</b> {權衡值_TSC}",
            "style": {"color": "white"}
        }
    )

    st.pydeck_chart(r)

    # 下方可以放個資料表格檢查一下
    if st.checkbox("顯示原始資料"):
        st.write(df)

except Exception as e:
    st.error(f"讀取檔案時出錯了：{e}")
    st.info("請確認 '3D出圖data.csv' 已經上傳到 GitHub 並且與 app.py 在同一個資料夾。")