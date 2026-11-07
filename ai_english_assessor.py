import streamlit as st
import pandas as pd
from datetime import datetime
import io
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
# Ô nhập API Key của anh
user_api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", placeholder="Dán API Key vào đây...")
st.sidebar.info("Hội thi “Ứng dụng công nghệ AI trong trường học” - Xã Thư Lâm 2026-2027")
st.sidebar.markdown("### 👨‍🏫 Thông tin")
st.sidebar.markdown("Hệ thống tích hợp Interactions API chuẩn (`gemini-3.8-flash`), chấm sâu theo Rubric chuẩn và xuất file Excel.")

st.title("🎯 Trợ lý ảo AI kiểm tra, đánh giá kỹ năng Nói & Viết Tiếng Anh THCS")
st.markdown("*Ứng dụng áp dụng Khung Rubric chuẩn, kết nối Interactions API để phân tích chuyên sâu, bóc tách lỗi sai và hiển thị kết quả trực tiếp.*")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "📝 Chấm bài Kỹ năng Viết (Writing)", 
    "🎤 Chấm bài Kỹ năng Nói (Speaking)", 
    "📊 Thống kê & Xuất Bảng Điểm"
])

with tab1:
    st.subheader("Chấm bài luận / Viết câu Tiếng Anh theo Khung Rubric chuẩn")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        student_name = st.text_input("Họ và tên học sinh:", placeholder="Ví dụ: Nguyễn Văn An", key="w_student_name")
    with col_info2:
        student_class = st.selectbox("Lớp:", ["Lớp 6A", "Lớp 6B", "Lớp 7A", "Lớp 7B", "Lớp 8A", "Lớp 9A"], key="w_class")
    with col_info3:
        grade_level = st.selectbox("Khối lớp chương trình:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], key="w_grade")

    # Gắn key riêng biệt để kiểm soát trạng thái dữ liệu nhập vào
    prompt_task = st.text_area("Đề bài / Yêu cầu viết (Prompt):", placeholder="Ví dụ: Write a paragraph about your future house.", key="w_prompt_task")
    student_writing = st.text_area("Bài làm thực tế của học sinh:", placeholder="Dán bài viết thực tế của học sinh vào đây...", height=150, key="w_student_writing")

    if st.button("🚀 Gửi AI chấm điểm theo Rubric chuyên sâu", type="primary"):
        if not user_api_key:
            st.error("⚠️ Vui lòng nhập Gemini API Key ở thanh sidebar bên trái trước khi chấm bài!")
        elif not student_name or not prompt_task or not student_writing:
            st.error("Vui lòng nhập đầy đủ: [Họ tên học sinh], [Đề bài] và [Bài làm thực tế]!")
        else:
            with st.spinner("🤖 Trợ lý AI đang áp dụng Khung Rubric chấm điểm chi tiết và bóc tách lỗi..."):
                try:
                    client = genai.Client(api_key=user_api_key)
                    
                    ai_prompt = f"""
                    Bạn là một giáo viên Tiếng Anh THCS chuyên môn cao tại Việt Nam. Hãy chấm điểm và phân tích bài viết thực tế sau của học sinh {student_name} ({grade_level}, chương trình Global Success) dựa chính xác trên Khung Rubric 4 tiêu chí sau (Thang điểm 10, mỗi tiêu chí 2.5 điểm):
                    
                    1. Task Achievement / Response (Hoàn thành yêu cầu đề bài - 2.5đ): Đánh giá độ đáp ứng yêu cầu đề, độ dài, bố cục ý chính, mức độ phát triển ý và mở rộng sáng tạo phù hợp lứa tuổi.
                    2. Coherence & Cohesion (Tính mạch lạc & Liên kết - 2.5đ): Đánh giá bố cục (Mở, Thân, Kết) và cách sử dụng từ nối (first, moreover, however, and, but, because...).
                    3. Lexical Resource (Từ vựng - 2.5đ): Đánh giá sự đa dạng từ vựng theo chủ điểm, collocations, word form và lỗi chính tả.
                    4. Grammatical Range & Accuracy (Ngữ pháp - 2.5đ): Đánh giá cấu trúc câu (đơn, ghép, phức theo cấp độ {grade_level}) và lỗi ngữ pháp (thì, mạo từ, số ít/nhiều, giới từ).
                    
                    - Đề bài thực tế: {prompt_task}
                    - Bài làm thực tế của học sinh: {student_writing}
                    
                    Hãy trả về kết quả bằng tiếng Việt theo định dạng Markdown rõ ràng gồm:
                    1. **🏆 KẾT QUẢ ĐÁNH GIÁ TỔNG QUAN:** Điểm tổng kết (thang 10), xếp loại (Xuất sắc, Khá/Tốt, Trung bình, Dưới chuẩn) và điểm chi tiết từng tiêu chí (thang 2.5đ).
                    2. **📊 ĐÁNH GIÁ CHI TIẾT TỪNG TIÊU CHÍ:** Nhận xét rõ ràng theo đúng chuẩn Rubric cho từng tiêu chí trên.
                    3. **🔍 BẢNG CHI TIẾT LỖI SAI TRONG BÀI:** Lập bảng gồm các cột: [STT | Trích đoạn câu gốc có lỗi | Loại lỗi | Phân tích bản chất lỗi | Hướng sửa đúng | Cấu trúc ngữ pháp áp dụng]. Phải bóc tách chính xác 100% các lỗi thực tế trong bài làm này.
                    4. **📈 GỢI Ý NÂNG CẤP TỪ VỰNG:** Đề xuất từ vựng/cụm từ nâng cao phù hợp với chủ đề để học sinh tiến bộ.
                    5. **💡 ĐOẠN VĂN MẪU HOÀN THIỆN:** Viết lại đoạn văn hoàn chỉnh, mượt mà bám sát ý tưởng của học sinh.
                    """
                    
                    interaction = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=ai_prompt
                    )
                    
                    ai_output = interaction.output_text
                    
                    st.success(f"✨ AI đã hoàn thành chấm điểm theo Rubric chuẩn cho học sinh: **{student_name}**!")
                    st.markdown("---")
                    st.markdown(ai_output)
                    
                    result_record = {
                        "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Họ và Tên": student_name,
                        "Lớp": student_class,
                        "Đề bài": prompt_task,
                        "Bài làm": student_writing,
                        "Trạng thái": "Đã chấm theo Rubric chuẩn"
                    }
                    st.session_state.student_results.append(result_record)
                    
                except Exception as e:
                    st.error(f"Lỗi khi gọi Interactions API: {str(e)}")

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
                    interaction = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=speaking_prompt
                    )
                    st.success(f"✨ Hoàn thành phân tích bài Nói cho em **{s_name}**!")
                    st.markdown("---")
                    st.markdown(interaction.output_text)
                except Exception as e:
                    st.error(f"Lỗi khi gọi Interactions API: {str(e)}")

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
