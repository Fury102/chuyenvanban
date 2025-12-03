import streamlit as st
import asyncio
import edge_tts
import tempfile
import os

async def text_to_speech(text, voice, rate):
    if rate >= 0:
        rate_str = f"+{rate}%"
    else:
        rate_str = f"{rate}%"
    communicate = edge_tts.Communicate(text, voice, rate=rate_str)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        await communicate.save(tmp_file.name)
        return tmp_file.name

def main():
    st.set_page_config(page_title="Text to Speech VN", page_icon="🇻🇳")
    st.title("Chuyển đổi Văn bản sang Giọng nói")

    text_input = st.text_area("Nhập văn bản cần đọc:", height=150, placeholder="Nhập nội dung tiếng Việt vào đây...")

    col1, col2 = st.columns(2)
    
    with col1:
        voice_option = st.selectbox(
            "Chọn giọng đọc:",
            ("Nữ (Hoài My)", "Nam (Nam Minh)")
        )
    
    with col2:
        speed = st.slider("Tốc độ đọc:", min_value=-50, max_value=50, value=0, step=10)

    if voice_option == "Nữ (Hoài My)":
        voice_code = "vi-VN-HoaiMyNeural"
    else:
        voice_code = "vi-VN-NamMinhNeural"

    if st.button("Xử lý & Tạo âm thanh", type="primary"):
        if text_input.strip():
            with st.spinner("Đang tạo file âm thanh..."):
                try:
                    audio_file = asyncio.run(text_to_speech(text_input, voice_code, speed))
                    
                    st.success("Đã tạo xong!")
                    st.audio(audio_file, format="audio/mp3")
                    
                    with open(audio_file, "rb") as f:
                        btn = st.download_button(
                            label="Tải xuống MP3",
                            data=f,
                            file_name="audio_output.mp3",
                            mime="audio/mp3"
                        )
                    
                    os.unlink(audio_file)
                except Exception as e:
                    st.error(f"Có lỗi xảy ra: {e}")
        else:
            st.warning("Vui lòng nhập văn bản trước.")

if __name__ == "__main__":
    main()