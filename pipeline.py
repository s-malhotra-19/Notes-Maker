import re
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai
import markdown
import os
from dotenv import load_dotenv

# ---------------------------------------------------------
# Extract YouTube Video ID
# ---------------------------------------------------------
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

# ---------------------------------------------------------
# Fetch transcript using YouTube Data API (CLOUD SAFE)
# ---------------------------------------------------------
def fetch_transcript_youtube_api(video_id, api_key):
    # 1. Get caption track list
    list_url = (
        f"https://www.googleapis.com/youtube/v3/captions?"
        f"videoId={video_id}&part=id&key={api_key}"
    )
    list_resp = requests.get(list_url)
    list_json = list_resp.json()

    if "items" not in list_json or len(list_json["items"]) == 0:
        raise ValueError("No captions available for this video.")

    caption_id = list_json["items"][0]["id"]

    # 2. Download caption file
    download_url = (
        f"https://www.googleapis.com/youtube/v3/captions/{caption_id}"
        f"?tfmt=ttml&key={api_key}"
    )
    dl_resp = requests.get(download_url)
    raw_text = dl_resp.text.strip()

    # 🔥 3. CHECK IF THE RESPONSE IS XML (TTML)
    if raw_text.startswith("<?xml") or raw_text.startswith("<tt"):
        # --- Parse as XML ---
        root = ET.fromstring(raw_text)
        text_segments = []
        for node in root.iter():
            if node.text:
                t = node.text.strip()
                if t:
                    text_segments.append(t)
        return "\n".join(text_segments)

    else:
        # --- Parse as Plain Text (SRT, VTT, etc.) ---
        lines = raw_text.splitlines()
        cleaned = []
        for line in lines:
            line = line.strip()
            # Skip timestamps and numbers
            if re.match(r"^\d+$", line): 
                continue
            if "-->" in line:  
                continue
            if line:
                cleaned.append(line)
        return "\n".join(cleaned)

# ---------------------------------------------------------
# Convert markdown → HTML file
# ---------------------------------------------------------
def markdown_to_html(md_text, output_file="notes.html"):
    html = markdown.markdown(md_text, extensions=["fenced_code", "tables", "nl2br"])
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    return output_file

# ---------------------------------------------------------
# MAIN FUNCTION: Generate Notes
# ---------------------------------------------------------
def generate_notes(url):
    # Load API keys
    load_dotenv()
    yt_api_key = os.getenv("YOUTUBE_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if yt_api_key is None:
        raise ValueError("YOUTUBE_API_KEY is missing.")
    if gemini_key is None:
        raise ValueError("GEMINI_API_KEY is missing.")

    # Extract video ID
    video_id = extract_video_id(url)

    # Fetch clean transcript (Cloud SAFE)
    transcript = fetch_transcript_youtube_api(video_id, yt_api_key)

    # Configure Gemini
    genai.configure(api_key=gemini_key)
    llm = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt for Gemini
    prompt = f"""
    Convert the following transcript into detailed, well-structured study notes.

    Follow these rules:
    - Use proper Markdown formatting
    - Include Headings & Subheadings
    - Add Bullet Points
    - Highlight key terms in **bold**
    - Use emojis where appropriate
    - Add a Summary at the end

    Transcript:
    {transcript}
    """

    # Generate response
    response = llm.generate_content(prompt)
    md_text = response.text

    # Convert to HTML
    html_path = markdown_to_html(md_text, "notes.html")

    return html_path
