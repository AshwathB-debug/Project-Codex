from Gemini import GeminiAPI
import os
from dotenv import load_dotenv
import streamlit as st
from pathlib import Path
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import tempfile
from pydub import AudioSegment
import pyttsx3


# def speechToText(audioFile):
#     r = sr.Recognizer()

#     try:

#         with sr.AudioFile(audioFile) as source:
#             audio = r.record(source)

#         message = r.recognize_google(audio)
#         message = message.lower()
#         return message

#     # Catch the timeout exception   
#     except sr.WaitTimeoutError:
        
#         print("No speech detected. Please try again.")
#         return None
    
#     except sr.UnknownValueError:
        
#         print("Sorry, I couldn't understand what you said.")    
#         return None

#     except sr.RequestError:
        
#         print("Speech recognition service unavailable.")
#         return None


def callTts(message):
    
    tts = pyttsx3.init() 
    tts.setProperty('rate', 150)
    voice = tts.getProperty("voices")
    tts.setProperty("voice", voice[1].id)
    tts.say(message)
    tts.runAndWait()
    

def textToSpeech(answer):
    
    while True:
        
        if answer:
            return callTts(answer)
        else:
            return callTts("No valid input received :( ")


def text_bubble(text, color, align, text_color):
    
    name = text.split(":")[0]
    message = text.split(":")[1]
    message = message.strip().replace("\n", "<br>")
    html = f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 10px; margin: 10px 0; text-align: left; display: inline-block; max-width: 80%; word-wrap: break-word;">
            <span style="font-size: 16px; font-weight: bold; color: {text_color};">{name}:</span> <span style="font-size: 16px; font-weight: normal; color: {text_color};">{message}</span>
        </div>
    """
        
    container = f"""
        <div style="width: 100%; display: flex; justify-content: {'flex-start' if align == 'left' else 'flex-end'};">
            {html}
        </div>
    """
    st.write(html, unsafe_allow_html=True)


def storeChat(chat, answer):
    
    if "History" not in st.session_state:
        st.session_state["History"] = []

    st.session_state["History"].append(("You", chat))
    st.session_state["History"].append(("Cody", answer))


def deployToSt(APIKEY):
    
    st.set_page_config(page_title = "Project Codex")
    
    st.markdown("""
    <style>
    h2 {
        color: #FFFFFF;
    }
    </style>""", unsafe_allow_html=True)
    
    st.header("Welcome to Project Codex!")

    if "History" not in st.session_state:
        st.session_state["History"] = []
    
    
    chat = st.chat_input("Chat with Cody: ")
    
    # audio = mic_recorder(
    #     start_prompt = "🎤",
    #     stop_prompt = "🚫",
    #     key = "mic_recorder",
    # )
    
    if chat:
        
        if chat.lower() == "clear".lower():
            st.session_state["History"] = []
            return
        
        gemini = GeminiAPI()
        answer = gemini.genAiModel(chat, APIKEY)
        
        if answer:
            storeChat(chat, answer)
            textToSpeech(answer)
    
    # elif audio:
    #     wav_file = None
        
    #     try:
    #         audio_segment = AudioSegment.from_file(io.BytesIO(audio['bytes']))
            
    #         with tempfile.NamedTemporaryFile(delete = False, suffix = ".wav") as tmpfile:
    #             audio_segment.export(tmpfile.name, format="wav")
    #             wav_file = tmpfile.name
                
    #         text = speechToText(wav_file)
            
    #         if text.lower() == "clear".lower():
    #             st.session_state["History"] = []
    #             return
        
    #         gemini = GeminiAPI()
    #         answer = gemini.genAiModel(text, APIKEY)
            
    #         if answer:
    #             storeChat(text, answer)
    #             textToSpeech(answer)
            
    #     except Exception as e:
    #         st.write(f"An error occurred during transcription: {e}")
        
    #     finally:
    #         if wav_file and os.path.exists(wav_file):
    #             os.remove(wav_file)
            

    # scrollable container for the chat history
    chat_history_column = st.columns([1])[0]
    with chat_history_column:
        
        if st.session_state["History"]:
            chat_history = ""
            
            for inp, out in st.session_state["History"]:
                
                if inp == "You":
                    text_bubble(f"{inp}: {out}", "#1F2022", "left", "#FFFFFF")
                    
                else:
                    text_bubble(f"{inp}: {out}", "#53565A", "right", "#FFFFFF")
                    
            st.markdown(f"<div style='height: 0px; overflow-y: auto; padding: 0px; border: 0px solid #ccc; "
                        f"border-radius: 10px;'>{chat_history}</div>", unsafe_allow_html=True)


# Main function automatically installs all the modules/packages from the requirements document and utilizes the API keys to call other functions
if __name__ == "__main__":
    
    # Load API keys and retrieve API key for Gemini API
    load_dotenv()
    APIKEY = os.getenv("APIKEY")
    deployToSt(APIKEY)