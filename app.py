import streamlit as st
import os
import uuid
import subprocess

# Cấu hình trang
st.set_page_config(page_title="Text to Speech VN", page_icon="🇻🇳")

def text_to_speech_cli(text, voice, rate):
    # Tạo tên file ngẫu nhiên
    output_file = f"audio_{uuid.uuid4()}.mp3"
    
    # Xử lý chuỗi tốc độ đọc (ví dụ: +20% hoặc -10%)
    rate_str = f"{rate:+d}%" 
    
    # Sử dụng subprocess để gọi lệnh edge-tts trực tiếp từ hệ thống
    # Cách này tránh hoàn toàn lỗi xung đột async trên Streamlit Cloud
    try:
        command = [
            "edge-tts",
            "--voice", voice,
            "--rate", rate_str,
            "--text", text,
            "--write-media", output_file
        ]
        
        # Chạy lệnh
        subprocess.run(command, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        st.error(f"Lỗi khi gọi lệnh TTS: {e}")
        return None
    except Exception as e:
        st.error(f"Lỗi không xác định: {e}")
        return None

def main():
    st.title("🇻🇳 Chuyển đổi Văn bản sang Giọng nói")
    st.caption("Chạy ổn định trên Streamlit Cloud")

    # Input văn bản
    text_input = st.text_area("Nhập văn bản (Tiếng Việt):", height=150, placeholder="Nhập nội dung vào đây...")

    col1, col2 = st.columns(2)
    
    with col1:
        voice_option = st.selectbox(
            "Chọn giọng đọc:",
            ("Nữ (Hoài My)", "Nam (Nam Minh)")
        )
    
    with col2:
        speed = st.slider("Tốc độ đọc (%):", min_value=-50, max_value=50, value=0, step=10)

    # Map tên giọng đọc
    if voice_option == "Nữ (Hoài My)":
        voice_code = "vi-VN-HoaiMyNeural"
    else:
        voice_code = "vi-VN-NamMinhNeural"

    if st.button("🔊 Tạo âm thanh", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ Vui lòng nhập văn bản!")
            return

        with st.spinner("Đang xử lý..."):
            audio_file = text_to_speech_cli(text_input, voice_code, speed)
            
            if audio_file and os.path.exists(audio_file):
                st.success("✅ Đã tạo xong!")
                
                # Hiển thị audio player
                st.audio(audio_file, format="audio/mp3")
                
                # Nút tải xuống
                with open(audio_file, "rb") as f:
                    file_bytes = f.read()
                    st.download_button(
                        label="⬇️ Tải file MP3",
                        data=file_bytes,
                        file_name="voice_output.mp3",
                        mime="audio/mp3"
                    )
                
                # Xóa file tạm
                os.remove(audio_file)
            else:
                st.error("Không thể tạo file âm thanh. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
