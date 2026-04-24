import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(layout="wide")
st.title("北北基桃交通權衡值 3D 視覺化 (起終點平均)")

# --- 1. 讀取與處理資料 ---
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '3D出圖data.csv')

try:
    df = pd.read_csv(file_path)
    
    # 數值轉換
    df['權衡值_TSC'] = pd.to_numeric(df['權衡值_TSC'], errors='coerce').fillna(0)
    
    # --- 核心邏輯：依照起點、終點分組並計算平均 ---
    # 同時保留經緯度 (取平均或第一個皆可，因為同地點經緯度相同)
    df_avg = df.groupby(['起點', '終點']).agg({
        '權衡值_TSC': 'mean',
        '終點經度': 'first',
        '終點緯度': 'first'
    }).reset_index()

    # --- 2. 設定 Pydeck 圖層 (ColumnLayer) ---
    layer = pdk.Layer(
        'ColumnLayer',
        data=df_avg,
        get_position='[終點經度, 終點緯度]',
        get_elevation='權衡值_TSC',
        radius=350,            # 增加半徑讓柱子更紮實
        elevation_scale=0.5,   # 降低高度縮放，讓整體變矮但保有差異
        get_fill_color='[80, 150, 200, 180]', # 改成藍色系增加透明質感
        pickable=True,
        extruded=True,
    )

    # --- 3. 設定攝影機視角 ---
    view_state = pdk.ViewState(
        latitude=df_avg['終點緯度'].mean(),
        longitude=df_avg['終點經度'].mean(),
        zoom=10.5,
        pitch=60, # 增加傾斜度，高低差會更明顯
    )

    # --- 4. 顯示地圖 ---
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>起點:</b> {起點}<br/><b>終點:</b> {終點}<br/><b>平均 TSC 權衡值:</b> {權衡值_TSC:.2f}",
            "style": {"color": "white"}
        }
    )

    st.pydeck_chart(r)

    if st.checkbox("顯示平均後的資料表格"):
        st.write(df_avg)

except Exception as e:
    st.error(f"執行出錯：{e}")