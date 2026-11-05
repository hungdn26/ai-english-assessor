import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import io
from google import genai

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Trợ lý AI Tiếng Anh THCS - Thuvien",
    page_icon="🎯",
    layout="wide"
)

# Khởi tạo bộ nhớ lưu trữ lịch sử chấm bài để xuất Excel thống kê
if 'student_results' not in st.session_state:
    st.session_state.student_results = []

st.sidebar.title("⚙️ Cấu hình hệ thống")
# Thêm ô nhập API Key để gọi AI thực tế
user_api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Hệ thống chấm bài Viết thông minh, gọi AI phân tích động 100% theo dữ liệu thực tế và xuất file Excel.")

st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng kết nối trực tiếp với mô hình AI để chấm điểm, bóc tách lỗi sai và gợi ý sửa đổi hoàn toàn dựa trên đề bài và bài làm thực tế của học sinh.*")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "📝 Chấm bài Kỹ năng Viết (Writing)", 
    "🎤 Chấm bài Kỹ năng Nói (Speaking)", 
    "📊 Thống kê & Xuất Bảng Điểm"
])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Phân tích động bằng AI thật)")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        student_name = st.text_input("Họ và tên học sinh:", placeholder="Ví dụ: Nguyễn Văn An")
    with col_info2:
        student_class = st.selectbox("Lớp:", ["Lớp 6A", "Lớp 6B", "Lớp 7A", "Lớp 7B", "Lớp 8A", "Lớp 9A"], key="w_class")
    with col_info3:
        grade_level = st.selectbox("Khối lớp chương trình:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")

    prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a short paragraph about your future house.")
    student_writing = st.text_area("Bài làm thực tế của học sinh:", placeholder="Dán bài viết thực tế của học sinh vào đây...", height=150)

    if st.button("🚀 Gửi AI phân tích và chấm điểm thực tế", type="primary"):
        if not student_name or not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ: [Họ tên học sinh], [Đề bài] và [Bài làm thực tế]!")
        else:
            with st.spinner("🤖 AI đang đọc hiểu đề bài và phân tích trực tiếp bài làm thực tế của học sinh..."):
                try:
                    # Khởi tạo client gọi AI thực tế
                    client = genai.Client(api_key=user_api_key) if user_api_key else genai.Client()
                    
                    # Prompt động chứa hoàn toàn dữ liệu thực tế của học sinh
                    dynamic_prompt = f"""
                    Bạn là một giáo viên và chuyên gia khảo thí Tiếng Anh THCS tại Việt Nam. 
                    Nhiệm vụ của bạn là chấm điểm và phân tích ĐÚNG VÀO NỘI DUNG THỰC TẾ do người dùng cung cấp dưới đây, tuyệt đối không dùng dữ liệu mẫu cũ.

                    - Họ tên học sinh: {student_name}
                    - Khối lớp: {grade_level}
                    - Đề bài thực tế: {prompt_task}
                    - Bài làm thực tế của học sinh: {student_writing}

                    Hãy trả về kết quả bằng tiếng Việt theo định dạng Markdown rõ ràng gồm các phần sau:
                    1. **Xác nhận đầu vào:** Nhắc lại ngắn gọn đề bài và bài làm thực tế của học sinh để đảm bảo tính đồng bộ.
                    2. **Điểm tổng quan & 4 tiêu chí IELTS (Thang điểm 10 / 2.5):** Đánh giá Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy căn cứ trực tiếp vào chất lượng thực tế của bài làm này.
                    3. **Bảng phân tích chi tiết tất cả lỗi sai:** Lập bảng gồm các cột: [STT | Trích đoạn câu gốc trong bài | Loại lỗi | Phân tích chi tiết bản chất lỗi | Hướng sửa đúng | Công thức / Cấu trúc ngữ pháp áp dụng]. Nếu bài có lỗi nào phải liệt kê đúng lỗi đó của chính bài làm này.
                    4. **Gợi ý nâng cấp từ vựng:** Đề xuất các từ vựng/cụm từ nâng cao phù hợp với chính chủ đề của đề bài này.
                    5. **Đoạn văn mẫu hoàn thiện:** Viết lại đoạn văn hoàn chỉnh, sửa sạch lỗi và giữ nguyên ý nghĩa cốt lõi của học sinh nhưng mượt mà, chuẩn ngữ pháp theo đúng đề bài.
                    """
                    
                    response = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=dynamic_prompt
                    )
                    
                    ai_result = response.output_text
                    
                    st.success(f"✨ Hoàn thành chấm bài bằng AI cho học sinh: **{student_name}**!")
                    st.markdown(ai_result)
                    
                    # Lưu kết quả vào session state để thống kê Excel
                    result_record = {
                        "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Họ và Tên": student_name,
                        "Lớp": student_class,
                        "Đề bài": prompt_task,
                        "Bài làm": student_writing,
                        "Kết quả AI": "Đã phân tích chi tiết thành công"
                    }
                    st.session_state.student_results.append(result_record)
                    
                except Exception as e:
                    st.error(f"Lỗi kết nối API AI: {e}. Vui lòng kiểm tra lại API Key ở sidebar bên trái hoặc kết nối mạng.")

with tab2:
    st.subheader("Chấm bài Nói Tiếng Anh (Speaking Assessment)")
    s_name = st.text_input("Họ và tên học sinh (Nói):", placeholder="Ví dụ: Trần Thị Mai")
    s_prompt = st.text_area("Đề bài nói (Speaking Prompt):", placeholder="Ví dụ: Talk about your favorite hobby.")
    transcript_text = st.text_area("Nội dung lời nói thực tế (Transcript):", placeholder="Nhập transcript thực tế của học sinh...", height=150)

    if st.button("🚀 Phân tích bài Nói thực tế", type="primary"):
        if not s_name or not s_prompt or not transcript_text:
            st.error("Vui lòng nhập đầy đủ [Họ tên], [Đề bài nói] và [Transcript]!")
        else:
            with st.spinner("🤖 Trợ lý AI đang phân tích bài nói thực tế..."):
                try:
                    client = genai.Client(api_key=user_api_key) if user_api_key else genai.Client()
                    speaking_prompt = f"""
                    Là giám khảo khảo thí Tiếng Anh THCS, hãy đánh giá bài nói thực tế sau của học sinh {s_name} khối nói:
                    - Đề bài nói: {s_prompt}
                    - Transcript thực tế: {transcript_text}
                    
                    Hãy trả về kết quả bằng tiếng Việt gồm: Điểm tổng quan, nhận xét chi tiết phát âm/từ vựng/ngữ pháp dựa trên chính transcript này, và câu trả lời mẫu cải thiện.
                    """
                    response = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=speaking_prompt
                    )
                    st.success(f"✨ Hoàn thành chấm bài Nói cho em **{s_name}**!")
                    st.markdown(response.output_text)
                except Exception as e:
                    st.error(f"Lỗi kết nối AI: {e}")

with tab3:
    st.subheader("📊 Quản lý kết quả học tập & Thống kê điểm số")
    st.markdown("Danh sách toàn bộ các bài làm thực tế của học sinh đã được hệ thống AI chấm điểm và lưu trữ:")
    
    if len(st.session_state.student_results) == 0:
        st.info("ℹ️ Chưa có dữ liệu bài làm nào được chấm. Vui lòng chấm bài ở tab 'Chấm bài Kỹ năng Viết' để hệ thống tổng hợp dữ liệu.")
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
