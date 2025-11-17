import streamlit as st
from pipeline import generate_notes  

st.title("YouTube Notes Generator")

url = st.text_input("Paste YouTube URL")

if st.button("Generate"):
    filepath = generate_notes(url)
    st.success("Notes generated!")

    with open(filepath, "r", encoding="utf-8") as f:
        st.download_button(
            "Download HTML",
            f,
            file_name="notes.html",
            mime="text/html"
        )
