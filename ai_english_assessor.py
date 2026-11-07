import streamlit as st
import pandas as pd
from datetime import datetime
import io
from PIL import Image
from google import genai

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
user_api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", placeholder="Dán API Key vào đây...")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Hệ thống tích hợp chuẩn `gemini-3.8-flash`, hỗ trợ chấm bài qua văn bản và ảnh chụp bài viết tay theo Rubric.")

st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng hỗ trợ chấm bài thông minh theo Khung Rubric chuẩn, kết nối trực tiếp mô hình gemini-3.8-flash.*")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "📝 Chấm bài Kỹ năng Viết (Writing)", 
    "🎤 Chấm bài Kỹ năng Nói (Speaking)", 
    "📊 Thống kê & Xuất Bảng Điểm"
])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Hỗ trợ Ảnh chụp & Văn bản)")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        student_name = st.text_input("Họ và tên học sinh:", placeholder="Ví dụ: Nguyễn Văn An", key="w_student_name")
    with col_info2:
        student_class = st.selectbox("Lớp:", ["Lớp 6A", "Lớp 6B", "Lớp 7A", "Lớp 7B", "Lớp 8A", "Lớp 9A"], key="w_class")
    with col_info3:
        grade_level = st.selectbox("Khối lớp chương trình:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")

    prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a paragraph about your future house.", key="w_prompt_task")
    
    input_method = st.radio("Chọn hình thức cung cấp bài làm của học sinh:", ["Nhập văn bản trực tiếp", "Tải lên ảnh chụp bài viết tay (Image)"], key="w_input_method")
    
    uploaded_image = None
    student_writing_text = ""

    if input_method == "Nhập văn bản trực tiếp":
        student_writing_text = st.text_area("Bài làm thực tế của học sinh:", placeholder="Dán bài viết thực tế của học sinh vào đây...", height=150, key="w_student_writing")
    else:
        uploaded_image = st.file_uploader("Tải lên ảnh chụp bài viết tay của học sinh (Định dạng: JPG, PNG, JPEG):", type=["jpg", "png", "jpeg"], key="w_uploaded_image")
        if uploaded_image is not None:
            image_obj = Image.open(uploaded_image)
            st.image(image_obj, caption=f"Ảnh bài làm của học sinh: {student_name if student_name else 'Chưa rõ tên'}", use_column_width=True)

    if st.button("🚀 Gửi AI phân tích chuyên sâu theo Rubric", type="primary"):
        if not user_api_key:
            st.error("⚠️ Vui lòng nhập Gemini API Key ở thanh sidebar bên trái trước khi chấm bài!")
        elif not student_name or not prompt_task or (input_method == "Nhập văn bản trực tiếp" and not student_writing_text) or (input_method == "Tải lên ảnh chụp bài viết tay (Image)" and uploaded_image is None):
            st.error("Vui lòng nhập đầy đủ thông tin: [Họ tên], [Đề bài] và [Bài làm / Ảnh chụp bài viết]!")
        else:
            with st.spinner("🤖 Trợ lý AI đang đọc hiểu bài làm và áp dụng Khung Rubric chấm điểm chi tiết..."):
                try:
                    # Khởi tạo client chuẩn
                    client = genai.Client(api_key=user_api_key)
                    
                    base_instruction = f"""
                    Bạn là một giáo viên Tiếng Anh THCS chuyên môn cao tại Việt Nam. Hãy chấm điểm và phân tích bài viết của học sinh {student_name} ({grade_level}, chương trình Global Success) dựa chính xác trên Khung Rubric 4 tiêu chí sau (Thang điểm 10, mỗi tiêu chí 2.5 điểm):
                    
                    1. Task Achievement / Response (Hoàn thành yêu cầu đề bài - 2.5đ): Đáp ứng yêu cầu đề, độ dài, bố cục ý chính, mức độ phát triển ý và mở rộng sáng tạo.
                    2. Coherence & Cohesion (Tính mạch lạc & Liên kết - 2.5đ): Bố cục (Mở, Thân, Kết) và cách sử dụng từ nối (first, moreover, however, and, but, because...).
                    3. Lexical Resource (Từ vựng - 2.5đ): Sự đa dạng từ vựng theo chủ điểm, collocations, word form và lỗi chính tả.
                    4. Grammatical Range & Accuracy (Ngữ pháp - 2.5đ): Cấu trúc câu (đơn, ghép, phức theo cấp độ {grade_level}) và lỗi ngữ pháp (thì, mạo từ, số ít/nhiều, giới từ).
                    
                    - Đề bài thực tế: {prompt_task}
                    """
                    
                    if input_method == "Nhập văn bản trực tiếp":
                        full_contents = [f"{base_instruction}\n- Bài làm thực tế của học sinh: {student_writing_text}\n\nHãy trả về kết quả bằng tiếng Việt theo định dạng Markdown rõ ràng gồm: 1. Kết quả đánh giá tổng quan & điểm chi tiết 4 tiêu chí. 2. Bảng chi tiết lỗi sai trong bài [STT | Trích câu gốc có lỗi | Loại lỗi | Bản chất lỗi | Hướng sửa đúng | Cấu trúc áp dụng]. 3. Gợi ý nâng cấp từ vựng. 4. Đoạn văn mẫu hoàn thiện."]
                    else:
                        image_data = Image.open(uploaded_image)
                        full_contents = [
                            f"{base_instruction}\n- Bài làm của học sinh được thể hiện trực tiếp qua ảnh chụp đính kèm. Hãy đọc kỹ nội dung viết tay trong ảnh để chấm điểm, sau đó trả kết quả chi tiết theo các phần yêu cầu.",
                            image_data
                        ]
                    
                    # Sử dụng hàm chuẩn models.generate_content để gọi model gemini-3.8-flash
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=full_contents
                    )
                    
                    ai_output = response.text
                    
                    st.success(f"✨ AI đã hoàn thành chấm điểm theo Rubric chuẩn cho học sinh: **{student_name}**!")
                    st.markdown("---")
                    st.markdown(ai_output)
                    
                    result_record = {
                        "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Họ và Tên": student_name,
                        "Lớp": student_class,
                        "Đề bài": prompt_task,
                        "Hình thức": "Ảnh chụp" if input_method == "Tải lên ảnh chụp bài viết tay (Image)" else "Văn bản",
                        "Trạng thái": "Đã chấm theo Rubric chuẩn"
                    }
                    st.session_state.student_results.append(result_record)
                    
                except Exception as e:
                    st.error(f"⚠️ Lỗi khi gọi API: {str(e)}")

with tab2:
    st.subheader("Chấm bài Nói Tiếng Anh (Speaking Assessment)")
    s_name = st.text_input("Họ và tên học sinh (Nói):", placeholder="Ví dụ: Trần Thị Mai", key="s_student_name")
    s_prompt = st.text_area("Đề bài nói (Speaking Prompt):", placeholder="Ví dụ: Talk about your favorite hobby.", key="s_prompt_task")
    transcript_text = st.text_area("Nội dung lời nói thực tế (Transcript):", placeholder="Nhập transcript thực tế của học sinh...", height=150, key="s_transcript")

    if st.button("🚀 AI phân tích bài Nói theo Rubric", type="primary"):
        if not user_api_key:
            st.error("⚠️ Vui lòng nhập Gemini API Key ở thanh sidebar bên trái!")
        elif not s_name or not s_prompt or not transcript_text:
            st.error("Vui lòng nhập đầy đủ [Họ tên], [Đề bài nói] và [Transcript]!")
        else:
            with st.spinner("🤖 Trợ lý AI đang chấm bài Nói..."):
                try:
                    client = genai.Client(api_key=user_api_key)
                    speaking_prompt = f"""
                    Là giám khảo khảo thí Tiếng Anh THCS, hãy đánh giá bài nói thực tế sau của học sinh {s_name} dựa trên Khung Rubric chuẩn:
                    - Đề bài nói: {s_prompt}
                    - Transcript thực tế: {transcript_text}
                    
                    Hãy trả về kết quả bằng tiếng Việt gồm: Điểm tổng quan, nhận xét chi tiết phát âm, từ vựng, ngữ pháp và câu trả lời mẫu cải thiện.
                    """
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=speaking_prompt
                    )
                    st.success(f"✨ Hoàn thành phân tích bài Nói cho em **{s_name}**!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"⚠️ Lỗi kết nối: {str(e)}")

with tab3:
    st.subheader("📊 Quản lý kết quả học tập & Thống kê điểm số")
    st.markdown("Danh sách toàn bộ các bài làm thực tế của học sinh đã được hệ thống AI chấm điểm theo Rubric và lưu trữ:")
    
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
