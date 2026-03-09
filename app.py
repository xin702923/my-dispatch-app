import streamlit as st
from docx import Document
import io
import re

# 1. 自動提取資訊的函數
def extract_fields(text):
    # 使用正則表達式抓取關鍵字後面的內容
    data = {}
    data['doc_no'] = re.search(r"文號[:：]\s*(\S+)", text).group(1) if re.search(r"文號[:：]\s*(\S+)", text) else ""
    data['doc_date'] = re.search(r"發文日期[:：]\s*(\S+)", text).group(1) if re.search(r"發文日期[:：]\s*(\S+)", text) else ""
    data['site_id'] = re.search(r"工地序號[:：]\s*(\S+)", text).group(1) if re.search(r"工地序號[:：]\s*(\S+)", text) else ""
    data['recv_id'] = re.search(r"收文序號[:：]\s*(\S+)", text).group(1) if re.search(r"收文序號[:：]\s*(\S+)", text) else ""
    data['recv_date'] = re.search(r"收文日期[:：]\s*(\S+)", text).group(1) if re.search(r"收文日期[:：]\s*(\S+)", text) else ""
    data['subject'] = re.search(r"主旨[:：]\s*([\s\S]+?)(?=時限|文件分類|$)", text).group(1).strip() if re.search(r"主旨[:：]\s*([\s\S]+?)(?=時限|文件分類|$)", text) else ""
    return data

# 2. 顯示網頁介面
st.title("📄 工地公文智慧產製系統")

uploaded_file = st.file_uploader("第一步：上傳公文掃描 PDF", type="pdf")

# 初始化欄位內容
extracted = {"doc_no": "", "doc_date": "", "site_id": "", "recv_id": "", "recv_date": "", "subject": ""}

if uploaded_file:
    # 這裡假設你已經串接好 OCR 辨識出 text
    raw_text = "文號: 國北都八1151006466 發文日期: 2026/3/5 工地序號: 收115-611 收文序號: 11216400 收文日期: 2026/3/5 主旨: 貴建築師提送安全監測工程..." 
    extracted = extract_fields(raw_text)
    st.success("自動偵測完成，請校對下方欄位")

# 第二步：欄位確認區
col1, col2, col3 = st.columns(3)
with col1:
    v_doc_no = st.text_input("文號", value=extracted['doc_no'])
    v_site_id = st.text_input("工地序號", value=extracted['site_id'])
with col2:
    v_doc_date = st.text_input("發文日期", value=extracted['doc_date'])
    v_recv_id = st.text_input("收文序號", value=extracted['recv_id'])
with col3:
    v_recv_date = st.text_input("收文日期", value=extracted['recv_date'])

v_subject = st.text_area("主旨", value=extracted['subject'])

# 第三步：自動勾選邏輯
st.subheader("知會人員")
is_safety = "安全" in v_subject or "監測" in v_subject
check_lin = st.checkbox("林博弘 (自動勾選)", value=is_safety)
check_wei = st.checkbox("魏志全 (自動勾選)", value=is_safety)

# 下載按鈕 (後續串接 Word 生成代碼...)
