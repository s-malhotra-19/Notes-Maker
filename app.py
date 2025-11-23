import streamlit as st
from pipeline import generate_notes
import time

# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="Nodeo – AI Notes Generator",
    page_icon="📝",
    layout="centered",
)

# -------------------------------------------------------------
# CUSTOM CSS (Professional UI)
# -------------------------------------------------------------
st.markdown("""
<style>
    .block-container {
        max-width: 680px;
        margin: auto;
        padding-top: 40px;
    }

    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #7c3aed;
        padding: 12px;
        font-size: 16px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        padding: 12px;
        font-size: 17px;
        font-weight: 600;
        transition: 0.2s ease;
        border: none;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        color: #888;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# HEADER
# -------------------------------------------------------------
st.markdown("<h1 style='text-align: center;'>📝 Nodeo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color:#6b6b6b;'>Smart notes from any YouTube lecture 🎓</p>", unsafe_allow_html=True)

# -------------------------------------------------------------
# INPUT
# -------------------------------------------------------------
url = st.text_input("🎥 Enter YouTube Link", placeholder="https://youtu.be/xyz123...")

generate = st.button("Generate Notes 🚀")

# -------------------------------------------------------------
# GENERATE LOGIC
# -------------------------------------------------------------
if generate:
    if not url.strip():
        st.error("❌ Please enter a valid YouTube URL.")
    else:
        with st.spinner("Processing your lecture… This may take a few seconds ⏳"):
            try:
                file_path = generate_notes(url)
                time.sleep(1)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()

        st.success("✔ Notes generated successfully!")

        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇ Download Notes (HTML)",
                data=f,
                file_name="notes.html",
                mime="text/html",
            )

# -------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------
st.markdown("<div class='footer'>Built with ❤️ by Nodeo</div>", unsafe_allow_html=True)
