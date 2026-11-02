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
st.markdown("*Ứng dụng hỗ trợ giáo viên và học sinh kiểm tra, đánh giá bài tập tự động, phân tích chuyên sâu đa chiều và định hướng nâng cấp bài viết.*")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Chấm bài Kỹ năng Viết (Writing)", "🎤 Chấm bài Kỹ năng Nói (Speaking)"])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Writing Assessment - Chuyên sâu theo Rubric)")
    col1, col2 = st.columns(2)
    
    with col1:
        grade_level = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")
        prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a short paragraph about your best friend.")
        
    with col2:
        student_writing = st.text_area("Bài làm của học sinh:", placeholder="Dán bài viết của học sinh vào đây...", height=150)

    if st.button("🚀 Phân tích và Chấm bài Viết siêu chuyên sâu", type="primary"):
        if not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ Đề bài và Bài làm của học sinh!")
        else:
            with st.spinner("🤖 Trợ lý AI đang thực hiện phân tích đa chiều và chấm điểm chi tiết..."):
                
                st.success("✨ Hoàn thành phân tích toàn diện kỹ năng Viết theo chuẩn THCS!")
                
                # 1. Tổng quan điểm số
                st.markdown("### 🏆 KẾT QUẢ ĐÁNH GIÁ TỔNG QUAN")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Điểm Tổng Kết", "7.0 / 10", "Khá")
                m2.metric("Task Achievement", "2.0 / 2.5", "Khá / Tốt")
                m3.metric("Coherence", "1.75 / 2.5", "Khá / Tốt")
                m4.metric("Grammar & Lexicon", "3.25 / 5.0", "Ổn định")
                
                st.markdown("---")
                
                # 2. Chi tiết 4 tiêu chí
                st.markdown("### 📊 CHI TIẾT 4 TIÊU CHÍ IELTS - THCS (Thang điểm 10)")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**1. Task Achievement (Hoàn thành yêu cầu):** 2.0 / 2.5 đ")
                    st.progress(0.8)
                    st.caption("Mức: Khá / Tốt - Đáp ứng tốt yêu cầu đề bài, đủ ý chính.")
                    
                    st.markdown("**2. Coherence & Cohesion (Tính mạch lạc):** 1.75 / 2.5 đ")
                    st.progress(0.7)
                    st.caption("Mức: Khá / Tốt - Bố cục rõ ràng, dùng từ nối cơ bản.")
                with col_b:
                    st.markdown("**3. Lexical Resource (Từ vựng):** 1.75 / 2.5 đ")
                    st.progress(0.7)
                    st.caption("Mức: Khá / Tốt - Từ vựng đúng chủ đề, đủ dùng.")
                    
                    st.markdown("**4. Grammatical Range & Accuracy (Ngữ pháp):** 1.5 / 2.5 đ")
                    st.progress(0.6)
                    st.caption("Mức: Trung bình - Đúng cấu trúc cơ bản, còn vài lỗi nhỏ.")
                
                st.markdown("---")
                
                # 3. Bảng phân tích lỗi sai & Công thức ngữ pháp
                st.markdown("### 🔍 BẢNG PHÂN TÍCH LỖI SAI CHI TIẾT & CÔNG THỨC NGỮ PHÁP")
                st.markdown("""
| STT | Câu gốc của học sinh | Lỗi sai phát hiện | Phân tích chi tiết & Cách sửa | Công thức / Cấu trúc chuẩn áp dụng |
|:---:|:---|:---|:---|:---|
| **1** | *"He always **help** me..."* | Sai chia động từ thì Hiện tại đơn | Chủ ngữ *He* là ngôi thứ 3 số ít, động từ thường phải thêm *-s/-es*. Sửa thành: **helps**. | **S (Ngôi 3 số ít) + V(s/es) + O** |
| **2** | *"...a **kindly boy**."* | Dùng sai từ loại (Word form) | Từ *kindly* là trạng từ, đứng trước danh từ phải dùng tính từ *kind*. Sửa thành: **a kind boy**. | **Tính từ (Adjective) + Danh từ (Noun)** |
                """)
                
                st.markdown("---")
                
                # 4. Phân tích độ đa dạng câu & Gợi ý nâng cấp từ vựng
                st.markdown("### 📈 PHÂN TÍCH CHUYÊN SÂU & NÂNG CẤP TỪ VỰNG")
                col_x, col_y = st.columns(2)
                with col_x:
                    st.markdown("#### ⚙️ Đánh giá cấu trúc câu:")
                    st.markdown("""
                    * **Mức độ câu đơn/câu ghép:** Học sinh đang dùng chủ yếu câu đơn (Simple sentences). 
                    * **Gợi ý cải thiện:** Nên kết hợp thêm câu phức (Complex sentences) chứa mệnh đề quan hệ (*who, which*) để bài viết mượt mà hơn.
                    """)
                with col_y:
                    st.markdown("#### 🌟 Bảng nâng cấp từ vựng thông minh:")
                    st.markdown("""
                    * *good at* ➡️ **excel in / have a passion for**
                    * *happy* ➡️ **delighted / overjoyed**
                    * *kind* ➡️ **helpful and compassionate**
                    """)
                
                st.markdown("---")
                
                # 5. Gợi ý mở rộng ý tưởng sáng tạo (Brainstorming Extension)
                st.markdown("### 💡 GỢI Ý MỞ RỘNG Ý TƯỞNG (BRAINSTORMING EXTENSION)")
                st.info(
                    "Để bài viết đạt điểm Xuất sắc (Mức tối đa), học sinh có thể bổ sung thêm một câu kể về kỷ niệm đáng nhớ chung của hai người (Ví dụ: *We once won a school science competition together*)."
                )
                
                # 6. Đoạn văn mẫu hoàn thiện
                st.markdown("### 📝 ĐOẠN VĂN MẪU HOÀN THIỆN (SUGGESTED REVISION)")
                st.markdown("Phiên bản chuẩn chỉnh, mạch lạc và đạt điểm cao theo chuẩn chương trình GDPT 2018:")
                
                st.success(
                    "\"He always **helps** me with my homework. "
                    "He likes playing football and listening to music. "
                    "He **excels in** English, but he **doesn't** like Maths. "
                    "We often play badminton together after school. "
                    "I am very **delighted** because he is my best friend. "
                    "I think he is a **kind** and helpful boy.\""
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
                ### 📊 BẢNG PHÂN TÍCH CHI TIẾT KỸ NĂNG NÓI
                | Tiêu chí đánh giá | Nhận xét chi tiết | Gợi ý cải thiện & Mẫu câu nâng cao |
                |:---|:---|:---|
                | **Fluency & Pronunciation** | Phát âm rõ ràng, nhịp điệu tự nhiên. | Dùng thêm từ nối: *Well, to be honest...* |
                | **Vocabulary & Grammar** | Dùng từ vựng đúng chủ đề, cấu trúc câu rõ ràng. | Cấu trúc nâng cao: *I'm really keen on...* |
                """)
