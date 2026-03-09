import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import re
from PIL import Image, ImageOps

def ocr_with_crop(pdf_bytes):
    # 1. 將 PDF 第一頁轉為高解析度圖片 (300 DPI 辨識手寫較準)
    images = convert_from_bytes(pdf_bytes, dpi=300, first_page=1, last_page=1)
    img = images[0]
    width, height = img.size

    # 2. 全域辨識 (抓文號、主旨、發文日期)
    full_text = pytesseract.image_to_string(img, lang='chi_tra+eng')

    # 3. 局部裁切 (抓左下角的手寫收文日期)
    # 座標範例：左側 0~30%, 下方 70~100% (視實際公文格式調整)
    left = 0
    top = int(height * 0.75) 
    right = int(width * 0.4)
    bottom = height
    crop_img = img.crop((left, top, right, bottom))
    
    # 強化圖片：轉灰階、提高對比，幫助辨識手寫
    crop_img = ImageOps.grayscale(crop_img)
    # 這裡可以視需求加入更多濾鏡
    
    # 單獨辨識左下角
    handwritten_text = pytesseract.image_to_string(crop_img, lang='chi_tra+eng', config='--psm 6')

    # 4. 解析資料
    data = {}
    data['doc_no'] = re.search(r"文\s*號[:：]\s*(\S+)", full_text).group(1) if re.search(r"文\s*號[:：]\s*(\S+)", full_text) else ""
    data['subject'] = re.search(r"主旨[:：]\s*([\s\S]+?)(?=說明|正本|$)", full_text).group(1).strip() if re.search(r"主旨[:：]\s*([\s\S]+?)(?=說明|正本|$)", full_text) else ""
    
    # 嘗試從手寫區抓日期 (例如 115/03/09)
    date_match = re.search(r"(\d{2,3}/\d{1,2}/\d{1,2})", handwritten_text)
    data['recv_date'] = date_match.group(1) if date_match else ""
    
    return data, img, crop_img

# --- UI 介面 ---
if uploaded_pdf:
    result, full_img, crop_img = ocr_with_crop(uploaded_pdf.read())
    
    st.image(full_img, caption="完整公文", use_container_width=True)
    
    with st.sidebar:
        st.subheader("🔍 手寫區域放大")
        st.image(crop_img, caption="左下角裁切範圍")
        st.write("若辨識不準，請直接修改下方欄位")

    # 填寫區... (同前一份程式碼)
