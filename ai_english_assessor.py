import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import io
import urllib.parse

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Trợ lý AI Tiếng Anh THCS - Thư Lâm",
    page_icon="🎯",
    layout="wide"
)

# Khởi tạo bộ nhớ lưu trữ lịch sử chấm bài để xuất Excel thống kê
if 'student_results' not in st.session_state:
    st.session_state.student_results = []

st.sidebar.title("⚙️ Cấu hình hệ thống")
st.sidebar.success("💡 Chế độ liên kết AI thông minh")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Hệ thống quản lý bài làm, định danh học sinh, xuất file Excel và tích hợp trợ lý AI.")

st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng kết hợp giao diện quản lý chuyên môn sư phạm và công cụ phân tích AI chuyên sâu.*")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "📝 Chấm bài Kỹ năng Viết (Writing)", 
    "🎤 Chấm bài Kỹ năng Nói (Speaking)", 
    "📊 Thống kê & Xuất Bảng Điểm"
])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Định danh & Kết nối AI)")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        student_name = st.text_input("Họ và tên học sinh:", placeholder="Ví dụ: Nguyễn Văn An")
    with col_info2:
        student_class = st.selectbox("Lớp:", ["Lớp 6A", "Lớp 6B", "Lớp 7A", "Lớp 7B", "Lớp 8A", "Lớp 9A"], key="w_class")
    with col_info3:
        grade_level = st.selectbox("Khối lớp chương trình:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")

    input_mode = st.radio("Chọn hình thức cung cấp bài làm:", ["Nhập văn bản trực tiếp", "Tải lên ảnh chụp bài viết tay (Image)"])
    prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a paragraph about your best friend.")
    
    student_writing = ""
    uploaded_image = None

    if input_mode == "Nhập văn bản trực tiếp":
        student_writing = st.text_area("Bài làm thực tế của học sinh:", placeholder="Dán bài viết thực tế của học sinh vào đây...", height=150)
    else:
        uploaded_image = st.file_uploader("Tải lên ảnh chụp bài viết tay của học sinh (JPG, PNG, JPEG):", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption=f"Ảnh chụp bài làm của học sinh: {student_name if student_name else 'Chưa rõ tên'}", use_column_width=True)
            student_writing = st.text_area("Nội dung văn bản trích xuất từ ảnh chụp:", placeholder="Nhập văn bản từ ảnh chụp...", height=100)

    if st.button("🚀 Tạo gói dữ liệu & Mở trung tâm phân tích AI", type="primary"):
        if not student_name or not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ: [Họ tên học sinh], [Đề bài] và [Bài làm thực tế]!")
        else:
            st.success(f"✨ Đã đóng gói dữ liệu thành công cho học sinh: **{student_name}** ({student_class})!")
            
            # Lưu vào lịch sử để xuất Excel
            result_record = {
                "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Họ và Tên": student_name,
                "Lớp": student_class,
                "Đề bài": prompt_task,
                "Bài làm": student_writing,
                "Trạng thái": "Đã xử lý & Lưu trữ"
            }
            st.session_state.student_results.append(result_record)
            
            st.markdown("---")
            st.markdown("### 📋 ĐÓNG GÓI CÂU LỆNH (PROMPT) CHẤM BÀI CHUYÊN SÂU")
            
            # Xây dựng nội dung prompt chuẩn chuyên môn
            prompt_content = f"""Hãy đóng vai trò là một giám khảo khảo thí Tiếng Anh THCS tại Việt Nam. Hãy chấm điểm và phân tích bài viết sau của học sinh {student_name} (Lớp {student_class}, {grade_level}) dựa trên Khung Rubric 4 tiêu chí IELTS (Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy):

- Đề bài: {prompt_task}
- Bài làm của học sinh: {student_writing}

Yêu cầu kết quả trả về bằng tiếng Việt gồm: Điểm tổng quan (thang 10), chi tiết 4 tiêu chí, bảng phân tích lỗi sai chi tiết kèm cấu trúc ngữ pháp, và đoạn văn mẫu hoàn thiện."""

            st.info("💡 Bạn có thể sao chép nhanh câu lệnh chuẩn dưới đây để dán vào trung tâm AI, hoặc bấm nút mở nhanh bên dưới:")
            st.code(prompt_content, language="markdown")
            
            # Nút liên kết mở nhanh sang Gemini web
            st.markdown(
                f'<a href="https://gemini.google.com/" target="_blank">'
                f'<button style="background-color:#4F46E5; color:white; padding:12px 20px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">'
                f'🔗 Mở ngay trang chủ Gemini AI để phân tích'
                f'</button></a>',
                unsafe_allow_html=True
            )

with tab2:
    st.subheader("Chấm bài Nói Tiếng Anh (Speaking Assessment)")
    s_name = st.text_input("Họ và tên học sinh (Nói):", placeholder="Ví dụ: Trần Thị Mai")
    s_prompt = st.text_area("Đề bài nói (Speaking Prompt):", placeholder="Ví dụ: Talk about your favorite hobby.")
    transcript_text = st.text_area("Nội dung lời nói thực tế (Transcript):", placeholder="Nhập transcript thực tế của học sinh...", height=150)

    if st.button("🚀 Tạo gói dữ liệu bài Nói", type="primary"):
        if not s_name or not s_prompt or not transcript_text:
            st.error("Vui lòng nhập đầy đủ [Họ tên], [Đề bài nói] và [Transcript]!")
        else:
            st.success(f"✨ Đã đóng gói bài nói cho em **{s_name}**!")
            speaking_query = f"Đánh giá bài nói Tiếng Anh cho học sinh {s_name}. Đề bài: {s_prompt}. Transcript: {transcript_text}"
            st.code(speaking_query, language="markdown")
            st.markdown(
                f'<a href="https://gemini.google.com/" target="_blank">'
                f'<button style="background-color:#4F46E5; color:white; padding:12px 20px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">'
                f'🔗 Mở ngay Gemini AI để phân tích bài Nói'
                f'</button></a>',
                unsafe_allow_html=True
            )

with tab3:
    st.subheader("📊 Quản lý kết quả học tập & Thống kê điểm số")
    st.markdown("Danh sách toàn bộ các bài làm thực tế của học sinh đã được hệ thống ghi nhận:")
    
    if len(st.session_state.student_results) == 0:
        st.info("ℹ️ Chưa có dữ liệu bài làm nào. Vui lòng thực hiện chấm bài ở tab 'Kỹ năng Viết'.")
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
