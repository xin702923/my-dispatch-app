import streamlit as st
import re
import io
from docx import Document

def refined_parse(raw_text):
    # 1. 預處理：統一全角半角符號，並處理可能的亂碼空格
    text = raw_text.replace('：', ':').replace('\xa0', ' ')
    
    # 2. 批次切割邏輯：以「文號:」作為每份公文的起點
    # 使用「正向預查」確保「文號」兩個字不會消失
    doc_blocks = re.split(r'(?=文號\s*[:])', text)
    
    results = []
    for block in doc_blocks:
        if "文號" not in block: continue
        
        info = {}
        # 3. 強化的正則表達式 (支援空格與不同換行)
        # 文號：抓取到下一個關鍵字或換行為止
        info['doc_no'] = re.search(r"文號\s*:\s*(\S+)", block).group(1) if re.search(r"文號\s*:\s*(\S+)", block) else ""
        
        # 日期：抓取 yyyy/mm/dd 或 yyy/mm/dd 格式
        info['doc_date'] = re.search(r"發文日期\s*:\s*([\d/]+)", block).group(1) if re.search(r"發文日期\s*:\s*([\d/]+)", block) else ""
        info['recv_date'] = re.search(r"收文日期\s*:\s*([\d/]+)", block).group(1) if re.search(r"收文日期\s*:\s*([\d/]+)", block) else ""
        
        # 序號：精準抓取「收」開頭的編號
        info['site_id'] = re.search(r"工地序號\s*:\s*(\S+)", block).group(1) if re.search(r"工地序號\s*:\s*(\S+)", block) else ""
        info['recv_id'] = re.search(r"收文序號\s*:\s*(\S+)", block).group(1) if re.search(r"收文序號\s*:\s*(\S+)", block) else ""
        
        # 主旨：最難抓的部分，設定明確的終止詞（如：時限、文件分類、組別）
        subj_match = re.search(r"主旨\s*[:]\s*([\s\S]+?)(?=時限|文件分類|組別|備註|$)", block)
        if subj_match:
            # 清理主旨內的換行與多餘空格，使其變成完整的一句話
            clean_subj = re.sub(r'\s+', '', subj_match.group(1))
            info['subject'] = clean_subj
        else:
            info['subject'] = ""
            
        results.append(info)
    return results

# --- Streamlit 介面優化 ---
st.title("🚀 精準版批次公文助手")
raw_input = st.text_area("請貼上公司網頁內容：", height=250)

if raw_input:
    data_list = refined_parse(raw_input)
    st.write(f"📊 系統偵測到 {len(data_list)} 筆資料")
    
    # 讓使用者可以「編輯」偵測後的結果，確保 100% 正確
    final_checked_data = []
    for i, item in enumerate(data_list):
        with st.expander(f"第 {i+1} 筆：{item['doc_no']}"):
            col1, col2 = st.columns(2)
            with col1:
                u_no = st.text_input(f"文號-{i}", value=item['doc_no'])
                u_s_id = st.text_input(f"工地序號-{i}", value=item['site_id'])
            with col2:
                u_date = st.text_input(f"發文日期-{i}", value=item['doc_date'])
                u_r_id = st.text_input(f"收文序號-{i}", value=item['recv_id'])
            u_subj = st.text_area(f"主旨-{i}", value=item['subject'])
            
            final_checked_data.append({
                "doc_no": u_no, "doc_date": u_date, "site_id": u_s_id,
                "recv_id": u_r_id, "subject": u_subj, "recv_date": item['recv_date']
            })
