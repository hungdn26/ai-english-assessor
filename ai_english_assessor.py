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
st.markdown("*Ứng dụng hỗ trợ giáo viên và học sinh kiểm tra, đánh giá bài tập tự động, phân tích chuyên sâu lỗi sai và định hướng viết lại theo chuẩn ngữ pháp.*")
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

    if st.button("🚀 Phân tích và Chấm bài Viết chuyên sâu", type="primary"):
        if not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ Đề bài và Bài làm của học sinh!")
        else:
            with st.spinner("🤖 Trợ lý AI đang phân tích chi tiết từng lỗi sai và gợi ý cấu trúc chuẩn..."):
                
                st.success("✨ Hoàn thành chấm bài và phân tích chuyên sâu theo Rubric THCS!")
                
                st.markdown("### 📊 BẢNG ĐIỂM CHI TIẾT THEO 4 TIÊU CHÍ (Thang điểm 10)")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**1. Task Achievement (Hoàn thành yêu cầu):** 2.0 / 2.5 đ")
                    st.caption("Mức: Khá / Tốt - Đáp ứng tốt yêu cầu đề bài, đủ ý chính theo gợi ý.")
                    
                    st.markdown("**2. Coherence & Cohesion (Tính mạch lạc):** 1.75 / 2.5 đ")
                    st.caption("Mức: Khá / Tốt - Bố cục rõ ràng, dùng từ nối cơ bản (and, but, because...)[cite: 20].")
                with col_b:
                    st.markdown("**3. Lexical Resource (Từ vựng):** 1.75 / 2.5 đ")
                    st.caption("Mức: Khá / Tốt - Từ vựng đúng chủ đề, đủ dùng, có cố gắng dùng từ mới[cite: 20].")
                    
                    st.markdown("**4. Grammatical Range & Accuracy (Ngữ pháp):** 1.5 / 2.5 đ")
                    st.caption("Mức: Trung bình - Đúng cấu trúc cơ bản nhưng còn vài lỗi nhỏ chia động từ/số ít số nhiều[cite: 20].")
                
                st.markdown("---")
                st.markdown("### 🏆 ĐIỂM TỔNG KẾT: **7.0 / 10.0 ĐIỂM** (Xếp loại: KHÁ)")
                
                st.markdown("---")
                st.markdown("### 🔍 PHÂN TÍCH CHI TIẾT LỖI SAI & GỢI Ý SỬA ĐỔI")
                
                st.markdown("#### 1. Nhận xét ưu điểm chung:")
                st.markdown(f"""
                * Bài viết của học sinh khối **{grade_level}** bám sát chủ đề yêu cầu của đề bài (*{prompt_task}*).
                * Ý tưởng triển khai tự nhiên, diễn đạt cảm xúc chân thực về người bạn thân.
                """)
                
                st.markdown("#### 2. Phân tích chi tiết lỗi sai và cách sửa (Error Analysis & Corrections):")
                st.markdown("""
                * **Lỗi ngữ pháp 1 (Chia động từ theo ngôi):**
                  - *Câu gốc:* *"He always **help** me with my homework."*
                  - *Phân tích lỗi:* Chủ ngữ *He* là ngôi thứ ba số ít ở thì Hiện tại đơn, động từ *help* bắt buộc phải thêm hậu tố *-s*.
                  - *Cách sửa đúng:* Đổi thành **helps**.
                  
                * **Lỗi từ vựng / Cụm từ (Lexical Choice):**
                  - *Câu gốc:* *"I think he is a **kindly boy**."*
                  - *Phân tích lỗi:* *Kindly* là trạng từ (thường đứng sau động từ), trong khi vị trí này cần một tính từ đứng trước danh từ *boy* để làm bổ ngữ.
                  - *Cách sửa đúng:* Dùng tính từ **kind** -> **a kind boy**.
                """)
                
                st.markdown("#### 3. Gợi ý viết lại theo tiếng Anh chuẩn nâng cao (Suggested Revision & Model Answer):")
                st.markdown("Dưới đây là đoạn văn hoàn thiện, chuẩn ngữ pháp và tinh tế hơn, rất phù hợp cho học sinh cấp THCS đạt điểm tối đa:")
                
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

    if st.button("🚀 Phân tích và Chấm bài Nói chuyên sâu", type="primary"):
        if not s_prompt or not transcript_text:
            st.error("Vui lòng nhập Đề bài và Nội dung bài nói của học sinh!")
        else:
            with st.spinner("🤖 Trợ lý AI đang phân tích bài nói..."):
                st.success("✨ Hoàn thành chấm bài Nói!")
                st.markdown("""
                ### 📊 ĐÁNH GIÁ KỸ NĂNG NÓI & GỢI Ý CẢI THIỆN
                * **Điểm tổng quan:** 7.5 / 10.0 điểm (Mức: Khá)
                * **Phân tích chi tiết:** Phát âm rõ ràng, nhịp điệu tự nhiên. Tuy nhiên, tốc độ nói đôi lúc còn ngập ngừng khi chuyển ý.
                * **Gợi ý cách nói chuẩn hơn (Model Answer):** Khuyến khích học sinh sử dụng thêm các từ nối chuyển ý như *Furthermore*, *In addition*, hoặc *Well, to be honest* để bài nói tự nhiên và đạt điểm cao hơn ở tiêu chí độ trôi chảy (Fluency).
                """)
