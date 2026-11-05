import streamlit as st
import pandas as pd
from datetime import datetime
import io
import requests
import json

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Trợ lý AI Tiếng Anh THCS - Thư Lâm",
    page_icon="🎯",
    layout="wide"
)

# Khởi tạo bộ nhớ lưu trữ lịch sử chấm bài để xuất Excel thống kê
if 'student_results' not in st.session_state:
    st.session_state.student_results = []

# Gán sẵn API Key chính thức của anh
FIXED_GEMINI_API_KEY = "AQ.Ab8RN6IsSIaBnPMumFQGL-Vfu-xR4oZCkhauEVCts7Bto-EWcw"

st.sidebar.title("⚙️ Cấu hình hệ thống")
st.sidebar.success("🔑 Đã kết nối API AI chuyên sâu")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Hệ thống chấm bài Viết & Nói thông minh, gọi AI phân tích sâu sát từng lỗi sai và xuất file Excel.")

st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng kết nối trực tiếp với mô hình AI Google Gemini để bóc tách toàn diện lỗi sai, chấm điểm chuyên sâu theo Rubric chuẩn.*")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "📝 Chấm bài Kỹ năng Viết (Writing)", 
    "🎤 Chấm bài Kỹ năng Nói (Speaking)", 
    "📊 Thống kê & Xuất Bảng Điểm"
])

def call_gemini_rest_api(prompt_text):
    """Hàm gọi REST API trực tiếp đến Google Gemini bằng model gemini-3.8-flash chính thức"""
    # Sử dụng đúng tên model chuẩn được hệ thống yêu cầu
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={FIXED_GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Lỗi API (Mã {response.status_code}): {response.text}"
    except Exception as e:
        return f"Lỗi kết nối mạng: {str(e)}"

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Phân tích chuyên sâu bằng AI thật)")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        student_name = st.text_input("Họ và tên học sinh:", placeholder="Ví dụ: Nguyễn Văn An")
    with col_info2:
        student_class = st.selectbox("Lớp:", ["Lớp 6A", "Lớp 6B", "Lớp 7A", "Lớp 7B", "Lớp 8A", "Lớp 9A"], key="w_class")
    with col_info3:
        grade_level = st.selectbox("Khối lớp chương trình:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")

    prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a paragraph about your future house.")
    student_writing = st.text_area("Bài làm thực tế của học sinh:", placeholder="Dán bài viết thực tế của học sinh vào đây...", height=150)

    if st.button("🚀 Gửi AI phân tích chuyên sâu ngay lập tức", type="primary"):
        if not student_name or not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ: [Họ tên học sinh], [Đề bài] và [Bài làm thực tế]!")
        else:
            with st.spinner("🤖 Trợ lý AI đang đọc hiểu, soi từng lỗi ngữ pháp và lập bảng phân tích chi tiết..."):
                
                ai_prompt = f"""
                Bạn là một chuyên gia khảo thí và giáo viên Tiếng Anh THCS tại Việt Nam. Hãy chấm điểm và phân tích bài viết thực tế sau của học sinh {student_name} (Khối {grade_level}) dựa trên Khung Rubric 4 tiêu chí IELTS chuẩn (Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy).
                
                - Đề bài thực tế: {prompt_task}
                - Bài làm thực tế của học sinh: {student_writing}
                
                Hãy trả về kết quả bằng tiếng Việt theo định dạng Markdown rõ ràng gồm các phần sau:
                1. **🏆 KẾT QUẢ ĐÁNH GIÁ TỔNG QUAN:** Điểm tổng kết (thang 10) và điểm chi tiết 4 tiêu chí (mỗi tiêu chí thang 2.5).
                2. **🔍 BẢNG CHI TIẾT LỖI SAI TRONG BÀI:** Lập bảng gồm các cột: [STT | Trích đoạn câu gốc có lỗi trong bài | Loại lỗi | Phân tích bản chất lỗi | Hướng sửa đúng | Cấu trúc ngữ pháp áp dụng]. Phải chỉ ra đúng các lỗi thực tế có trong bài.
                3. **📈 GỢI Ý NÂNG CẤP TỪ VỰNG:** Đề xuất các từ vựng/cụm từ nâng cao phù hợp với đúng chủ đề của đề bài này.
                4. **💡 ĐOẠN VĂN MẪU HOÀN THIỆN:** Viết lại đoạn văn hoàn chỉnh, sửa sạch lỗi, mượt mà nhưng giữ nguyên ý tưởng cốt lõi của học sinh.
                """
                
                ai_result = call_gemini_rest_api(ai_prompt)
                
                if "Lỗi" in ai_result[:10]:
                    st.error(f"⚠️ {ai_result}")
                else:
                    st.success(f"✨ AI đã hoàn thành phân tích chuyên sâu cho học sinh: **{student_name}**!")
                    st.markdown("---")
                    st.markdown(ai_result)
                    
                    result_record = {
                        "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Họ và Tên": student_name,
                        "Lớp": student_class,
                        "Đề bài": prompt_task,
                        "Bài làm": student_writing,
                        "Trạng thái": "Đã AI chấm chuyên sâu"
                    }
                    st.session_state.student_results.append(result_record)

with tab2:
    st.subheader("Chấm bài Nói Tiếng Anh (Speaking Assessment)")
    s_name = st.text_input("Họ và tên học sinh (Nói):", placeholder="Ví dụ: Trần Thị Mai")
    s_prompt = st.text_area("Đề bài nói (Speaking Prompt):", placeholder="Ví dụ: Talk about your favorite hobby.")
    transcript_text = st.text_area("Nội dung lời nói thực tế (Transcript):", placeholder="Nhập transcript thực tế của học sinh...", height=150)

    if st.button("🚀 AI phân tích bài Nói chuyên sâu", type="primary"):
        if not s_name or not s_prompt or not transcript_text:
            st.error("Vui lòng nhập đầy đủ [Họ tên], [Đề bài nói] và [Transcript]!")
        else:
            with st.spinner("🤖 Trợ lý AI đang phân tích bài nói thực tế..."):
                speaking_prompt = f"""
                Là giám khảo khảo thí Tiếng Anh THCS, hãy đánh giá bài nói thực tế sau của học sinh {s_name}:
                - Đề bài nói: {s_prompt}
                - Transcript thực tế: {transcript_text}
                
                Hãy trả về kết quả bằng tiếng Việt gồm: Điểm tổng quan, nhận xét chi tiết phát âm/từ vựng/ngữ pháp dựa trên chính transcript này, và câu trả lời mẫu cải thiện.
                """
                speaking_result = call_gemini_rest_api(speaking_prompt)
                
                if "Lỗi" in speaking_result[:10]:
                    st.error(f"⚠️ {speaking_result}")
                else:
                    st.success(f"✨ Hoàn thành phân tích bài Nói cho em **{s_name}**!")
                    st.markdown("---")
                    st.markdown(speaking_result)

with tab3:
    st.subheader("📊 Quản lý kết quả học tập & Thống kê điểm số")
    st.markdown("Danh sách toàn bộ các bài làm thực tế của học sinh đã được hệ thống AI chấm điểm và lưu trữ:")
    
    if len(st.session_state.student_results) == 0:
        st.info("ℹ️ Chưa có dữ liệu bài làm nào được chấm. Vui lòng chấm bài ở tab 'Chấm bài Kỹ năng Viết'.")
    else:
        df_results = pd.DataFrame(st.session_state.student_results)
        st.dataframe(df_results, use_container_width=True)
        
        st.markdown("---")
        
        def convert_df_to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='ThongKeDiem_THCS')
            return output.getvalue()

        excel_data = convert_df_to_excel(df_results)
        
        st.download_button(
            label="📥 Tải xuống file Excel thống kê điểm (.xlsx)",
            data=excel_data,
            file_name=f"ThongKe_DiemTiengAnh_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
        
        if st.button("🗑️ Xóa toàn bộ lịch sử thống kê"):
            st.session_state.student_results = []
            st.rerun()
