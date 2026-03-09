import streamlit as st
from docx import Document
import io

# 網頁標題
st.set_page_config(page_title="工地公文自動化系統", layout="wide")
st.title("📄 公文派示單自動產生器")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    doc_type = st.selectbox("文件類型", ["正式函文", "備忘錄"])
    st.info("上傳工地掃描檔，系統將自動填寫派示單")

# 上傳區
uploaded_file = st.file_uploader("請上傳公文 PDF 掃描檔", type="pdf")

if uploaded_file is not None:
    st.success("檔案上傳成功！正在進行 OCR 辨識...")
    
    # 這裡放辨識邏輯 (模擬辨識結果)
    doc_no = "國北都八1151006466" 
    subject = "安全監測工程施工計畫書（修正一版）"
    
    # 顯示辨識結果讓用戶確認
    col1, col2 = st.columns(2)
    with col1:
        new_doc_no = st.text_input("確認文號", value=doc_no)
    with col2:
        new_date = st.date_input("發文日期")

    new_subject = st.text_area("確認主旨", value=subject)

    # 自動勾選邏輯
    st.subheader("知會人員 (系統已根據主旨自動預選)")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    # 邏輯判斷：若主旨有「施工」則預設勾選
    is_construction = "施工" in new_subject
    p1 = col_p1.checkbox("林博弘", value=is_construction)
    p2 = col_p2.checkbox("魏志全", value=is_construction)
    p3 = col_p3.checkbox("范嘉文", value=False)

    # 下載按鈕
    if st.button("產生並下載 Word 派示單"):
        # 這裡執行填寫 Word 的程式碼 (如之前提供的 python-docx 邏輯)
        st.balloons()
        st.download_button("點我下載檔案", data="...", file_name="派示單.docx")
