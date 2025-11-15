import os
from dotenv import load_dotenv
import requests
from langchain_community.document_loaders import WebBaseLoader
from uuid import uuid4
import streamlit as st


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser




load_dotenv()


# 🧩 Setup Streamlit UI
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast Agent", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast Agent")


# Sidebar for keys
st.sidebar.header("🔑 API Keys")
gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")


keys_provided = all([gemini_api_key, elevenlabs_api_key])
if not keys_provided:
    st.warning("Please provide all API keys to continue.")


# User input
url = st.text_input("Enter Blog URL:")
generate_button = st.button("🎙️ Generate Podcast", disabled=not keys_provided)


def scrape_blog(url):
    """Scrape and return blog content."""
    loader = WebBaseLoader(url)
    docs = loader.load()
    return " ".join([d.page_content for d in docs])


def summarize_blog(blog_text, api_key):
    """Summarize the blog content into a short podcast-style script."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=gemini_api_key)

    prompt = ChatPromptTemplate.from_template(
        """
        You are a creative podcast scriptwriter 🎙️.
        Summarize the following blog content into an engaging, conversational, and friendly 2-minute podcast script.
        Keep it **under 2000 characters**.
        
        Blog Content:
        {blog_content}
        """
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"blog_content": blog_text})

def text_to_speech_elevenlabs(text, api_key, voice_id="BFvr34n3gOoz0BAf9Rwn"):
    """Convert summarized text to audio using ElevenLabs."""
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"  
    }
    payload = {
        "model_id": "eleven_multilingual_v2",
        "text": text
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"ElevenLabs API Error: {response.text}")

if generate_button:
    if not url.strip():
        st.warning("Please enter a blog URL first.")
    else:
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        os.environ["ELEVENLABS_API_KEY"] = elevenlabs_api_key

        with st.spinner("🎧 Scraping blog, summarizing, and generating podcast..."):
            try:
                blog_text = scrape_blog(url)
                summary = summarize_blog(blog_text, gemini_api_key)
                audio_bytes = text_to_speech_elevenlabs(summary, elevenlabs_api_key)

                # Save and display
                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)
                filename = f"{save_dir}/podcast_{uuid4()}.mp3"

                with open(filename, "wb") as f:
                    f.write(audio_bytes)

                st.success("Podcast generated successfully! 🎙️")
                st.audio(audio_bytes, format="audio/mp3")

                st.download_button(
                    label="Download Podcast",
                    data=audio_bytes,
                    file_name="generated_podcast.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
