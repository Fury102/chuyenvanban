import streamlit as st
import os
import uuid
import subprocess
import sys
from gtts import gTTS

# Cấu hình trang
st.set_page_config(page_title="Text to Speech VN", page_icon="🇻🇳")

def tts_google(text):
    """Sử dụng Google Translate TTS - Luôn ổn định"""
    try:
        output_file = f"audio_google_{uuid.uuid4()}.mp3"
        tts = gTTS(text=text, lang='vi')
        tts.save(output_file)
        return output_file, None
    except Exception as e:
        return None, str(e)

def tts_microsoft(text, voice, rate):
    """Sử dụng Microsoft Edge TTS - Giọng hay nhưng dễ bị chặn IP"""
    output_file = f"audio_ms_{uuid.uuid4()}.mp3"
    rate_str = f"{rate:+d}%"
    
    # Dùng sys.executable để gọi python environment chính xác hơn
    command = [
        sys.executable, "-m", "edge_tts",
        "--voice", voice,
        "--rate", rate_str,
        "--text", text,
        "--write-media", output_file
    ]
    
    try:
        # capture_output=True để bắt lỗi chi tiết nếu có
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            return output_file, None
        else:
            # Trả về lỗi chi tiết từ server Microsoft
            return None, result.stderr
    except Exception as e:
        return None, str(e)

def main():
    st.title("🇻🇳 Chuyển đổi Văn bản sang Giọng nói")
    
    # Input văn bản
    text_input = st.text_area("Nhập văn bản:", height=150, placeholder="Nhập nội dung tiếng Việt vào đây...")

    # Cấu hình
    col1, col2 = st.columns(2)
    with col1:
        server_option = st.selectbox(
            "Chọn máy chủ:",
            ("Server Google (Luôn chạy ok)", "Server Microsoft (Giọng hay - Dễ lỗi)")
        )
    
    voice_code = None
    speed = 0
    
    # Chỉ hiển thị tùy chọn giọng/tốc độ nếu chọn Microsoft
    if "Microsoft" in server_option:
        with col2:
            voice_select = st.selectbox("Giọng đọc:", ("Nữ (Hoài My)", "Nam (Nam Minh)"))
            speed = st.slider("Tốc độ:", -50, 50, 0, 10)
            
        if "Hoài My" in voice_select:
            voice_code = "vi-VN-HoaiMyNeural"
        else:
            voice_code = "vi-VN-NamMinhNeural"
    else:
        st.info("ℹ️ Server Google chỉ có 1 giọng mặc định và tốc độ chuẩn.")

    # Nút xử lý
    if st.button("🔊 Tạo âm thanh", type="primary"):
        if not text_input.strip():
            st.warning("Vui lòng nhập văn bản!")
            return

        with st.spinner("Đang tạo file..."):
            if "Microsoft" in server_option:
                audio_file, error = tts_microsoft(text_input, voice_code, speed)
            else:
                audio_file, error = tts_google(text_input)

            # Xử lý kết quả
            if audio_file and os.path.exists(audio_file):
                st.success("✅ Thành công!")
                st.audio(audio_file, format="audio/mp3")
                
                with open(audio_file, "rb") as f:
                    st.download_button("⬇️ Tải file MP3", f, "audio.mp3", "audio/mp3")
                
                os.remove(audio_file) # Dọn dẹp
            else:
                st.error("❌ Lỗi tạo file!")
                if error:
                    with st.expander("Xem chi tiết lỗi"):
                        st.code(error)
                    if "Microsoft" in server_option:
                        st.warning("💡 Gợi ý: Server Microsoft đang chặn IP Cloud. Hãy chuyển sang chọn 'Server Google' ở trên để dùng tạm.")

if __name__ == "__main__":
    main()
