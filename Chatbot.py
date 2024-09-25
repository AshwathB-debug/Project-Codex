from pathlib import Path

import convo
import speech_recognition as sr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pyttsx3
import streamlit as st


def userSpeech():
    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

            audio = recognizer.listen(source, timeout=5)  # Set the timeout to 5 seconds
            message = recognizer.recognize_google(audio)
            message = message.lower()
            return message

            # Catch the timeout exception   
    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.")
        return None

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None

    except sr.RequestError:
        print("Speech recognition service unavailable.")
        return None


def listOfExitWords():
    exit_words = [
        "quit",
        "exit",
        "bye",
        "goodbye",
        "stop",
        "end",
        "done",
        "finished",
        "close",
        "terminate"
    ]

    return exit_words


def joinWordsInOutput(output):
    arr = []
    for word in output:
        arr.append(word.text)
    response = " ".join(arr)

    return response


# Set up the model
def generationConfig():
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192}

    return generation_config


# Sets the settings to block explicit content
def safetySettings():
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT",
         "threshold": "BLOCK_MEDIUM_AND_ABOVE"},

        {"category": "HARM_CATEGORY_HATE_SPEECH",
         "threshold": "BLOCK_MEDIUM_AND_ABOVE"},

        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
         "threshold": "BLOCK_MEDIUM_AND_ABOVE"},

        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
         "threshold": "BLOCK_MEDIUM_AND_ABOVE"}]

    return safety_settings


def genAiModel(chat, apiKey):
    try:
        genai.configure(api_key=apiKey)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generationConfig(),
                                      safety_settings=safetySettings())
        convo = model.start_chat(history=[])
        output = convo.send_message(chat, stream=True)

        if "search" and "local" and "file" in joinWordsInOutput(output):
            st.write(LocalFileCalling())

        return joinWordsInOutput(output)


    except Exception as e:
        print(f"An error occurred {e}")
        return None


def speakToCody():
    while True:

        userMessage = userSpeech()

        if "search" and "local" and "file" in userMessage:
            LocalFileCalling()

        if userMessage:

            if any(statement in userMessage.lower() for statement in listOfExitWords()):
                convo.send_message(userMessage)
                print("Cody: " + convo.last.text)
                callTts(convo.last.text)
                return "Success"
                break

            convo.send_message(userMessage)
            print("Cody: " + convo.last.text)
            callTts(convo.last.text)


        else:

            print("Cody: No valid input received :( ")
            callTts("No valid input received :( ")


def callTts(message):
    tts = pyttsx3.init()
    # tts.setProperty('rate', 75)
    voice = tts.getProperty("voices")
    tts.setProperty("voice", voice[0].id)
    tts.say(message)
    tts.runAndWait()


def LocalFileCalling():
    current_directory = Path.cwd()
    print("Current Directory:", current_directory)
    print("\n")
    # the root tells us the current directory, dirs will list the directories in this directory, and the files will list the files in the directory
    file_found = False  # keeps track of if file is found or not
    st.write("Caps matter, type the name and the filetype ex:(bot.py)")
    name = input("Enter filename): ", )  # Add chatinput feature so that user can type that filename within streamlit

    for root, dirs, files in os.walk(f"{current_directory}"):

        for files in files:

            if files.endswith(name):
                return "FOUND THE FILE: " + files
                file_found = True

    if file_found == False:
        return "File not found"


def text_bubble(text, color, align, text_color):
    name = text.split(":")[0]
    message = text.split(":")[1]
    html = f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 10px; text-align: {align};">
            <span style="font-size: 16px; font-weight: bold; color: {text_color};">{name}:</span> <span style="font-size: 16px; font-weight: normal; color: {text_color};">{message}</span>
        </div>
        """
    st.write(html, unsafe_allow_html=True)


def deployToSt(APIKEY):
    st.set_page_config(page_title="Project Codex")
    st.header("Welcome to Project Codex!")
    st.write("<i>[tip: type clear to erase chat]</i>", unsafe_allow_html=True)

    if "History" not in st.session_state:
        st.session_state["History"] = []

    chat = st.chat_input("Type to Cody: ")

    if chat:
        # if chat.lower() in [exit_w.lower() for exit_w in listOfExitWords()]:
        if chat.lower() == "clear".lower():
            st.session_state["History"] = []
            return
        answer = genAiModel(chat, APIKEY)
        if answer:
            # st.subheader("Chat History")
            storeChat(chat, answer)

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


def storeChat(chat, answer):
    if "History" not in st.session_state:
        st.session_state["History"] = []

    st.session_state["History"].append(("You", chat))
    st.session_state["History"].append(("Cody", answer))


def main():
    os.system("pip install -r requirements.txt")
    print("\n Downloaded the required directories \n")
    load_dotenv()
    # API key for Gemini API
    APIKEY = os.getenv("APIKEY")
    # API key for Weather API
    APIKEY2 = os.getenv("APIKEY2")
    deployToSt(APIKEY)


if __name__ == "__main__":
    main()
