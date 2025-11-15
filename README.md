# 📰 ➡️ 🎙️ Blog-to-Podcast Agent

Convert any blog article into an engaging podcast episode using AI! This project leverages **LangChain**, **Google Gemini LLM**, and **ElevenLabs TTS** to automatically summarize blogs and generate natural-sounding audio.

---

## 🚀 Live Demo
Check out the live app: [Blog-to-Podcast]((https://blog-to-podcast-agent.streamlit.app/))

---

## 🛠️ Features

- AI-powered summarization of blog content into a concise, conversational podcast script.  
- Uses **LangChain pipelines** for web scraping and content processing.  
- Generates realistic podcast audio with **ElevenLabs Text-to-Speech API**.  
- Interactive **Streamlit UI** for real-time blog-to-audio conversion and downloads.  

---

## 💻 Tech Stack

- **Frontend / UI:** Streamlit  
- **LLM / Summarization:** Google Gemini (`langchain-google-genai`)  
- **Web Scraping:** LangChain Community `WebBaseLoader`  
- **Text-to-Speech:** ElevenLabs API  
- **Programming Language:** Python  
- **Utilities:** `dotenv`, `uuid4`, `requests`  

---

## ⚙️ Setup & Installation

1. Clone the repository:

```bash
git clone https://github.com/Shailesh2003-arch/Blog-to-Podcast.git
cd Blog-to-Podcast
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run main.py
```

### 📝 Usage

- Enter your Gemini API Key and ElevenLabs API Key in the sidebar.
- Paste the blog URL you want to convert.
- Click 🎙️ Generate Podcast.
- Listen to the generated podcast and download it using the built-in download button.

