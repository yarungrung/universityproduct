import streamlit as st
import pandas as pd

# 1. 讀取 Excel 檔案
# 假設你的檔案名稱是 data.xlsx
df = pd.read_excel('大專生計畫rawdata.xlsx')

# 2. 轉換成 JSON
# orient='records' 會讓輸出的格式像這樣：[{"欄位1": "值1"}, {"欄位1": "值2"}]
# force_ascii=False 是為了確保中文不會變成亂碼
json_str = df.to_json(orient='records', force_ascii=False, indent=4)

# 3. 儲存成 .json 檔
with open('大專生計畫rawdata.json', 'w', encoding='utf-8') as f:
    f.write(json_str)

print("轉換成功！")

# 1. 使用 st.Page() 定義所有頁面
# 注意：st.Page() 會自動尋找 .py 檔案
pages = [
   st.Page("page_home.py", title="首頁", icon="🏠"),
   st.Page("page_3dmap-1.py", title="「國土分區」的Pydeck 3D互動地圖瀏覽", icon="🌏"),
   st.Page("page_3dmap-2.py", title="「國土利用」Pydeck 3D互動地圖瀏覽", icon="ℹ️")
]

# 2. 使用 st.navigation() 建立導覽 (例如在側邊欄)
with st.sidebar:
    st.title("此為大專生計畫成果展示：")
    # st.navigation() 會回傳被選擇的頁面
    selected_page = st.navigation(pages)


# 3. 執行被選擇的頁面
selected_page.run()