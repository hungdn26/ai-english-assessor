import streamlit as st
from PIL import Image
from google import genai

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Trợ lý AI Tiếng Anh THCS - Thư Lâm",
    page_icon="🎯",
    layout="wide"
)

st.sidebar.title("⚙️ Cấu hình hệ thống")
user_api_key = st.sidebar.text_input("Nhập Gemini API Key:", value="AQ.Ab8RN6LdbVoHJvz6NB9VpAR4wwfBOL6uvfUGvDGxGf4mapxfBA", type="password")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Hệ thống chấm bài Viết tự động hoàn toàn dựa trên dữ liệu thực tế của học sinh.")

st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng tự động chấm điểm, bóc tách lỗi sai và gợi ý sửa đổi hoàn toàn dựa trên đề bài và bài làm thực tế của học sinh.*")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Chấm bài Kỹ năng Viết (Writing)", "🎤 Chấm bài Kỹ năng Nói (Speaking)"])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh (Chấm điểm động theo thực tế)")
    
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        grade_level = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")
    with col_cfg2:
        input_mode = st.radio("Chọn hình thức nộp bài:", ["Nhập văn bản trực tiếp", "Tải lên ảnh chụp bài viết tay (Image)"])

    prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a short paragraph about your best friend.")
    
    student_writing = ""
    uploaded_image = None

    if input_mode == "Nhập văn bản trực tiếp":
        student_writing = st.text_area("Bài làm của học sinh:", placeholder="Dán bài viết thực tế của học sinh vào đây...", height=150)
    else:
        uploaded_image = st.file_uploader("Tải lên ảnh chụp bài viết tay của học sinh (Format: JPG, PNG, JPEG):", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Ảnh chụp bài viết tay của học sinh", use_column_width=True)
            # Tạm thời để trống để người dùng nhập hoặc nếu dùng Vision API sẽ trích xuất sau, ở đây ta ưu tiên lấy văn bản nhập thực tế
            student_writing = st.text_area("Nội dung văn bản trích xuất từ ảnh (hoặc chỉnh sửa nếu cần):", placeholder="Nhập lại nội dung từ ảnh chụp...", height=100)

    if st.button("🚀 Chấm điểm và phân tích theo bài làm thực tế", type="primary"):
        if not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ Đề bài và Bài làm thực tế của học sinh!")
        else:
            with st.spinner("🤖 AI đang phân tích trực tiếp đề bài và bài làm thực tế của học sinh..."):
                try:
                    client = genai.Client(api_key=user_api_key) if user_api_key else genai.Client()
                    
                    # Prompt yêu cầu AI chấm động hoàn toàn dựa trên dữ liệu đầu vào thực tế
                    dynamic_prompt = f"""
                    Bạn là một giáo viên và chuyên gia khảo thí Tiếng Anh THCS tại Việt Nam. 
                    Nhiệm vụ của bạn là chấm điểm và phân tích ĐÚNG VÀO NỘI DUNG THỰC TẾ do người dùng cung cấp dưới đây, tuyệt đối không bịa đặt hay dùng dữ liệu mẫu cũ.

                    - Khối lớp: {grade_level}
                    - Đề bài thực tế: {prompt_task}
                    - Bài làm thực tế của học sinh: {student_writing}

                    Hãy trả về kết quả bằng tiếng Việt theo định dạng Markdown rõ ràng gồm các phần sau:
                    1. **Xác nhận đầu vào:** Nhắc lại ngắn gọn đề bài và bài làm thực tế của học sinh để đảm bảo tính đồng bộ.
                    2. **Điểm tổng quan & 4 tiêu chí IELTS (Thang điểm 10 / 2.5):** Đánh giá Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy căn cứ trực tiếp vào chất lượng thực tế của bài làm.
                    3. **Bảng phân tích chi tiết tất cả lỗi sai:** Lập bảng gồm các cột: [STT | Trích đoạn câu gốc trong bài | Loại lỗi | Phân tích chi tiết bản chất lỗi | Hướng sửa đúng | Công thức / Cấu trúc ngữ pháp áp dụng]. Nếu bài có lỗi nào phải liệt kê đúng lỗi đó của chính bài làm này.
                    4. **Gợi ý nâng cấp từ vựng:** Đề xuất các từ vựng/cụm từ nâng cao phù hợp với chính chủ đề của đề bài này.
                    5. **Đoạn văn mẫu hoàn thiện:** Viết lại đoạn văn hoàn chỉnh, sửa sạch lỗi và giữ nguyên ý nghĩa cốt lõi của học sinh nhưng mượt mà, chuẩn ngữ pháp theo đúng đề bài.
                    """
                    
                    response = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=dynamic_prompt
                    )
                    
                    st.success("✨ Hoàn thành chấm bài thành công!")
                    st.markdown(response.output_text)
                    
                except Exception as e:
                    st.error(f"Lỗi kết nối AI: {e}. Vui lòng kiểm tra lại API Key hoặc mạng internet.")

with tab2:
    st.subheader("Chấm bài Nói Tiếng Anh (Speaking Assessment)")
    st.markdown("*(Nhập nội dung văn bản chuyển đổi từ giọng nói của học sinh để AI phân tích)*")
    
    col1, col2 = st.columns(2)
    with col1:
        s_grade = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="s_grade")
        s_prompt = st.text_area("Đề bài nói (Speaking Prompt):", placeholder="Ví dụ: Talk about your favorite hobby.")
    with col2:
        transcript_text = st.text_area("Nội dung lời nói của học sinh (Transcript):", placeholder="Nhập văn bản transcript thực tế của học sinh...", height=150)

    if st.button("🚀 Phân tích bài Nói thực tế", type="primary"):
        if not s_prompt or not transcript_text:
            st.error("Vui lòng nhập Đề bài và Nội dung bài nói thực tế!")
        else:
            with st.spinner("🤖 Trợ lý AI đang phân tích bài nói thực tế..."):
                try:
                    client = genai.Client(api_key=user_api_key) if user_api_key else genai.Client()
                    speaking_prompt = f"""
                    Là giám khảo khảo thí Tiếng Anh THCS, hãy đánh giá bài nói thực tế sau của học sinh khối {s_grade}:
                    - Đề bài nói: {s_prompt}
                    - Transcript thực tế: {transcript_text}
                    
                    Hãy trả về kết quả bằng tiếng Việt gồm: Điểm tổng quan, nhận xét chi tiết phát âm/từ vựng/ngữ pháp dựa trên chính transcript này, và câu trả lời mẫu cải thiện.
                    """
                    response = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=speaking_prompt
                    )
                    st.success("✨ Hoàn thành phân tích bài Nói!")
                    st.markdown(response.output_text)
                except Exception as e:
                    st.error(f"Lỗi kết nối AI: {e}")
