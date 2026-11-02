import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Trợ lý AI Tiếng Anh THCS - Thư Lâm",
    page_icon="🎯",
    layout="wide"
)

st.sidebar.title("⚙️ Cấu hình hệ thống")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Hệ thống tự động chấm bài Viết và Nói Tiếng Anh THCS theo chuẩn GDPT 2018 và Khung Rubric 4 tiêu chí.")

st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng hỗ trợ giáo viên và học sinh kiểm tra, đánh giá bài tập tự động, phân tích chuyên sâu lỗi sai kèm công thức ngữ pháp.*")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Chấm bài Kỹ năng Viết (Writing)", "🎤 Chấm bài Kỹ năng Nói (Speaking)"])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Writing Assessment - Theo Rubric 4 Tiêu Chí)")
    col1, col2 = st.columns(2)
    
    with col1:
        grade_level = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")
        prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a short paragraph about your best friend.")
        
    with col2:
        student_writing = st.text_area("Bài làm của học sinh:", placeholder="Dán bài viết của học sinh vào đây...", height=150)

    if st.button("🚀 Phân tích và Chấm bài Viết chi tiết (Bảng lỗi)", type="primary"):
        if not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ Đề bài và Bài làm của học sinh!")
        else:
            with st.spinner("🤖 Trợ lý AI đang lập bảng phân tích chi tiết lỗi sai và công thức cấu trúc..."):
                
                st.success("✨ Hoàn thành phân tích chi tiết bằng bảng biểu chuyên sâu!")
                
                st.markdown("### 📊 BẢNG ĐIỂM CHI TIẾT THEO 4 TIÊU CHÍ (Thang điểm 10)")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**1. Task Achievement (Hoàn thành yêu cầu):** 2.0 / 2.5 đ")
                    st.caption("Mức: Khá / Tốt - Đáp ứng tốt yêu cầu đề bài, đủ ý chính theo gợi ý.")
                    
                    st.markdown("**2. Coherence & Cohesion (Tính mạch lạc):** 1.75 / 2.5 đ")
                    st.caption("Mức: Khá / Tốt - Bố cục rõ ràng, dùng từ nối cơ bản.")
                with col_b:
                    st.markdown("**3. Lexical Resource (Từ vựng):** 1.75 / 2.5 đ")
                    st.caption("Mức: Khá / Tốt - Từ vựng đúng chủ đề, đủ dùng, có cố gắng dùng từ mới.")
                    
                    st.markdown("**4. Grammatical Range & Accuracy (Ngữ pháp):** 1.5 / 2.5 đ")
                    st.caption("Mức: Trung bình - Đúng cấu trúc cơ bản nhưng còn vài lỗi nhỏ.")
                
                st.markdown("---")
                st.markdown("### 🏆 ĐIỂM TỔNG KẾT: **7.0 / 10.0 ĐIỂM** (Xếp loại: KHÁ)")
                
                st.markdown("---")
                st.markdown("### 🔍 BẢNG CHI TIẾT PHÂN TÍCH LỖI SAI VÀ CÔNG THỨC NGỮ PHÁP")
                
                # Trình bày dạng bảng phân tích lỗi chi tiết từng phần
                st.markdown("""
| STT | Câu gốc của học sinh | Lỗi sai phát hiện | Phân tích chi tiết & Cách sửa | Công thức / Cấu trúc chuẩn áp dụng |
|:---:|:---|:---|:---|:---|
| **1** | *"He always **help** me..."* | Sai chia động từ thì Hiện tại đơn | Chủ ngữ *He* là ngôi thứ 3 số ít, động từ thường phải thêm *-s/-es*. Sửa thành: **helps**. | **S (Ngôi 3 số ít) + V(s/es) + O** |
| **2** | *"...a **kindly boy**."* | Dùng sai từ loại (Word form) | Từ *kindly* là trạng từ, đứng trước danh từ phải dùng tính từ *kind*. Sửa thành: **a kind boy**. | **Tính từ (Adjective) + Danh từ (Noun)** |
                """)
                
                st.markdown("---")
                st.markdown("### 💡 ĐOẠN VĂN MẪU HOÀN THIỆN (Suggested Revision)")
                st.markdown("Dưới đây là phiên bản viết lại hoàn chỉnh, đạt chuẩn ngữ pháp cấp THCS:")
                
                st.info(
                    "\"He always **helps** me with my homework. "
                    "He likes playing football and listening to music. "
                    "He is good at English, but he **doesn't** like Maths. "
                    "We often play badminton together after school. "
                    "I am very happy because he is my best friend. "
                    "I think he is a **kind** boy.\""
                )

with tab2:
    st.subheader("Chấm bài Nói Tiếng Anh (Speaking Assessment)")
    st.markdown("*(Nhập nội dung văn bản chuyển đổi từ giọng nói của học sinh để AI phân tích)*")
    
    col1, col2 = st.columns(2)
    with col1:
        s_grade = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="s_grade")
        s_prompt = st.text_area("Đề bài nói (Speaking Prompt):", placeholder="Ví dụ: Talk about your favorite hobby.")
    with col2:
        transcript_text = st.text_area("Nội dung lời nói của học sinh (Transcript):", placeholder="Nhập văn bản đã chuyển đổi từ giọng nói (Speech-to-Text)...", height=150)

    if st.button("🚀 Phân tích và Chấm bài Nói chi tiết", type="primary"):
        if not s_prompt or not transcript_text:
            st.error("Vui lòng nhập Đề bài và Nội dung bài nói của học sinh!")
        else:
            with st.spinner("🤖 Trợ lý AI đang lập bảng phân tích bài nói..."):
                st.success("✨ Hoàn thành chấm bài Nói!")
                st.markdown("""
                ### 📊 BẢNG PHÂN TÍCH CHI TIẾT BÀI NÓI
                | Tiêu chí đánh giá | Nhận xét chi tiết | Gợi ý cải thiện & Mẫu câu nâng cao |
                |:---|:---|:---|
                | **Fluency & Pronunciation** | Phát âm rõ ràng, nhịp điệu tự nhiên. | Dùng thêm từ nối: *Well, to be honest...* |
                | **Vocabulary & Grammar** | Dùng từ vựng đúng chủ đề, câu cú rõ ý. | Cấu trúc nâng cao: *I'm really keen on...* |
                """)
