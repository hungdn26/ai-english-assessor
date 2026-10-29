import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="AI English Assessment Assistant - Thư Lâm",
    page_icon="🤖",
    layout="wide"
)

# Cài đặt sẵn API Key trực tiếp (để không phải nhập lại mỗi lần chạy)
genai.configure(api_key="AQ.Ab8RN6IEq5Qy7TK8-cIBcsgiVdSi6iLW-CsiJB3c_vxQg_UXQg")
model = genai.GenerativeModel('gemini-3.8-flash')

# Thanh bên (Sidebar) hướng dẫn
st.sidebar.title("⚙️ Hướng dẫn")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Trợ lý ảo tự động chấm bài Viết và Nói Tiếng Anh THCS, phân tích lỗi sai và gợi ý cải thiện theo chuẩn GDPT 2018.")

# Tiêu đề chính
st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng hỗ trợ giáo viên chấm bài tự động, phân tích lỗi ngữ pháp, phát âm theo chuẩn GDPT 2018.*")
st.markdown("---")

# Chọn tab chức năng: Kỹ năng Viết hoặc Nói
tab1, tab2 = st.tabs(["📝 Chấm bài Kỹ năng Viết (Writing)", "🎤 Chấm bài Kỹ năng Nói (Speaking)"])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Writing Assessment)")
    col1, col2 = st.columns(2)
    
    with col1:
        grade_level = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")
        prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a short paragraph about your best friend.")
        
    with col2:
        student_writing = st.text_area("Bài làm của học sinh:", placeholder="Dán bài viết của học sinh vào đây...", height=150)

    if st.button("🚀 Phân tích và Chấm bài Viết", type="primary"):
        if not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ Đề bài và Bài làm của học sinh!")
        else:
            with st.spinner("🤖 AI đang phân tích ngữ pháp, từ vựng và cấu trúc bài viết..."):
                try:
                    prompt_content = f"""
                    Bạn là một giáo viên và chuyên gia khảo thí Tiếng Anh THCS tại Việt Nam. Hãy chấm điểm và nhận xét bài viết sau đây của học sinh khối {grade_level}.
                    Đề bài: {prompt_task}
                    Bài làm của học sinh: {student_writing}
                    
                    Hãy trả về kết quả bằng tiếng Việt theo cấu trúc rõ ràng sau:
                    1. **Điểm tổng quan (Thang điểm 10):** Đánh giá dựa trên tiêu chí Task Achievement, Coherence, Vocabulary, Grammar.
                    2. **Nhận xét ưu điểm:** Khen ngợi những điểm tốt trong bài.
                    3. **Phân tích lỗi sai chi tiết (Error Analysis):** Chỉ ra rõ các lỗi chính tả, ngữ pháp, cấu trúc câu và giải thích tại sao sai.
                    4. **Gợi ý sửa đổi (Suggested Revision):** Viết lại đoạn văn mẫu đạt điểm cao, phù hợp lứa tuổi học sinh THCS.
                    """
                    response = model.generate_content(prompt_content)
                    st.success("✨ Hoàn thành chấm bài!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi khi kết nối với AI: {e}")

with tab2:
    st.subheader("Chấm bài Nói Tiếng Anh (Speaking Assessment)")
    st.markdown("*(Nhập nội dung văn bản chuyển đổi từ giọng nói của học sinh để AI phân tích)*")
    
    col1, col2 = st.columns(2)
    with col1:
        s_grade = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="s_grade")
        s_prompt = st.text_area("Đề bài nói (Speaking Prompt):", placeholder="Ví dụ: Talk about your favorite hobby.")
    with col2:
        transcript_text = st.text_area("Nội dung lời nói của học sinh (Transcript):", placeholder="Nhập văn bản đã chuyển đổi từ giọng nói (Speech-to-Text)...", height=150)

    if st.button("🚀 Phân tích và Chấm bài Nói", type="primary"):
        if not s_prompt or not transcript_text:
            st.error("Vui lòng nhập Đề bài và Nội dung bài nói của học sinh!")
        else:
            with st.spinner("🤖 AI đang phân tích độ trôi chảy, từ vựng và phát âm..."):
                try:
                    speaking_prompt = f"""
                    Bạn là một giám khảo khảo thí Tiếng Anh chuyên nghiệp cấp THCS. Hãy đánh giá bài nói dựa trên transcript sau của học sinh khối {s_grade}.
                    Đề bài nói: {s_prompt}
                    Nội dung bài nói (Transcript): {transcript_text}
                    
                    Hãy trả về kết quả bằng tiếng Việt theo cấu trúc:
                    1. **Điểm tổng quan (Thang điểm 10):** Đánh giá theo tiêu chí Fluency, Pronunciation, Vocabulary, Grammar.
                    2. **Đánh giá nội dung & Từ vựng:** Nhận xét ý tưởng và cách dùng từ.
                    3. **Lỗi ngữ pháp & Cấu trúc cần khắc phục:** Chỉ ra lỗi sai cụ thể trong câu nói.
                    4. **Gợi ý cải thiện (Model Answer):** Cung cấp câu trả lời mẫu tự nhiên, hay hơn cho học sinh luyện tập.
                    """
                    response = model.generate_content(speaking_prompt)
                    st.success("✨ Hoàn thành chấm bài Nói!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi khi kết nối với AI: {e}")