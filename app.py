import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""
You are youtube video summarizer. You will be taking the transcript text and summarizing the entire video and
providing the important summary in points within 250 words. Please provide the summary of the text given here:  
"""
#Getting Transcript DAta from the youtube video
def extract_transcrpit_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for trans in transcript_text:
            transcript+=" "+trans["text"]
        return transcript
    except Exception as e:
        raise e


def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# if youtube_link:
#     video_id=youtube_link.split("=")[1]
#     print(video_id)
#     st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if youtube_link:
    video_id = youtube_link.split("=")[1]
    image_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    
    # Set the desired width and height
    width = 300  # in pixels
    height = 200  # in pixels
    
    st.markdown(
        f'<img src="{image_url}" width="{width}" height="{height}">',
        unsafe_allow_html=True
    )


if st.button("Get Detailed Notes"):
    transcript_text=extract_transcrpit_details(youtube_link)
    
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)



