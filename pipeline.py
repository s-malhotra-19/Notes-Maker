import re
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import markdown
import os
from dotenv import load_dotenv


# the function below is extracting the video id from the given provided youtube link
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")


#our ai api is giving the output in markdown and we are converting it to html 
def markdown_to_html(md_text, output_file="notes.html"):
    html = markdown.markdown(md_text, extensions=["fenced_code", "tables", "nl2br"])
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    return output_file

#this is doing the main work of making the notes 
def generate_notes(url):
    # Extract video ID
    video_id = extract_video_id(url)

    # Fetch transcript
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en", "hi"])

    # Setup Gemini
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    llm = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt
    prompt = f"""
    Clean this transcript and convert it into detailed study notes.

    Use Markdown formatting:
    - Headings, subheadings
    - Bold text
    - Bullet points
    - Emojis
    - Summary

    Transcript:
    {transcript}
    """

    response = llm.generate_content(prompt)
    md_text = response.text

    # Convert to HTML
    html_path = markdown_to_html(md_text, "notes.html")

    return html_path

import joblib

