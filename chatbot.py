import streamlit as st
import google.generativeai as genai


st.set_page_config(
    page_title="🤖 ChatBot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Chatbot Kzn")
st.caption("Based Google Gemini & Streamlit")

st.sidebar.header("Pengaturan")
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.sidebar.success("API Key berhasil dimuat!", icon="✅")
except (FileNotFoundError, KeyError):
    api_key = st.sidebar.text_input("Masukkan Google API Key Anda:", type="password")

if not api_key:
    st.info("Silakan masukkan Google API Key Anda di sidebar untuk memulai.")
    st.stop()

# --- Inisialisasi Model Gemini ---
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Terjadi kesalahan saat mengkonfigurasi API. Pastikan API Key Anda valid. Detail: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:

    system_prompt = {
        "role": "user",
        "parts": ["Kamu adalah Kzn, asisten AI yang sangat ramah, cerdas, dan selalu membantu. Jawablah semua pertanyaan dalam Bahasa Indonesia dengan gaya bahasa yang natural dan mudah dimengerti."]
    }
    response_prompt = {
        "role": "model",
        "parts": ["Tentu! Halo, saya Kzn. Senang bertemu denganmu! Ada yang bisa saya bantu hari ini?"]
    }

    st.session_state.chat = model.start_chat(history=[system_prompt, response_prompt])
    st.session_state.messages.append({"role": "assistant", "content": response_prompt["parts"][0]})

def clear_chat_history():
    """Fungsi untuk mereset state percakapan."""
    keys_to_delete = ["messages", "chat"]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
    
st.sidebar.button("Mulai Percakapan Baru", on_click=clear_chat_history)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Apa yang ingin Anda tanyakan?"):
    # Menampilkan pesan pengguna
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Menambahkan pesan pengguna ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.spinner("Kzn sedang mengetik..."):
            response = st.session_state.chat.send_message(prompt, stream=False)
        
        if response and response.parts:
            
            response_text = response.parts[0].text
            
     
            with st.chat_message("assistant"):
                st.markdown(response_text)

            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:    fallback_response = "Maaf, saya tidak dapat memberikan respons untuk itu. Coba pertanyaan lain."
            
            with st.chat_message("assistant"):
                st.markdown(fallback_response)
            

    except Exception as e:
        # Menangani error teknis lainnya
        error_message = f"Maaf, terjadi masalah teknis: {str(e)}"
        st.error(error_message)
        # Menambahkan pesan error ke UI agar pengguna tahu
        st.session_state.messages.append({"role": "assistant", "content": error_message})
