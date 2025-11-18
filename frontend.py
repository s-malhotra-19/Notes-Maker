import streamlit as st
from pipeline import generate_notes
import time
import base64

# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="Nodeo – AI Notes Generator",
    page_icon="📝",
    layout="centered",
)

# -------------------------------------------------------------
# CUSTOM CSS (Professional Vibes)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Center everything */
    .block-container {
        max-width: 680px;
        margin: auto;
        padding-top: 40px;
    }

    /* Input box styling */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #7c3aed;
        padding: 12px;
        font-size: 16px;
    }

    /* Primary button */
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

    /* Card container */
    .result-box {
        background: #fafafa;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        margin-top: 20px;
    }

    /* Footer */
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
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>📝 Nodeo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color:#6b6b6b;'>Smart notes from any YouTube lecture 🎓</p>", unsafe_allow_html=True)

st.write("")
st.write("")


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

        # Read file
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # # ---------------------------------------------------------
        # # PREVIEW (Styled Box)
        # # ---------------------------------------------------------
        # st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        # st.markdown("### 📄 Preview (HTML Notes)")
        # st.components.v1.html(html_content, height=400, scrolling=True)
        # st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # DOWNLOAD BUTTON
        # ---------------------------------------------------------
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
