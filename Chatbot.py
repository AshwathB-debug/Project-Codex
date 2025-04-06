from Gemini import GeminiAPI
import os
import sys
from dotenv import load_dotenv
import streamlit as st
from pathlib import Path
import requests
import speech_recognition as sr



# def userSpeech():
#     recognizer = sr.Recognizer()

#     try:

#         with sr.Microphone() as source:
#             recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

#             audio = recognizer.listen(source, timeout=5)  # Set the timeout to 5 seconds
#             message = recognizer.recognize_google(audio)
#             message = message.lower()
#             return message

#             # Catch the timeout exception   
#     except sr.WaitTimeoutError:
        
#         print("No speech detected. Please try again.")
#         return None


#     except sr.UnknownValueError:
        
#         print("Sorry, I couldn't understand what you said.")
#         return None

#     except sr.RequestError:
        
#         print("Speech recognition service unavailable.")
#         return None



# def weatherStack(APIKEY2):
    
#     url = "https://api.weatherstack.com/current?access_key={APIKEY2}"
#     location = {"query" : """ Add the input function here """}
#     response = requests.get(url, params = location)
#     return response.json()



# def listOfFunctions(function):
    
#     tupOfFunctions = ("OVERVIEW", "INCOME_STATEMENT", "BALANCE_SHEET", "CASH_FLOW", "EARNINGS")
#     return function in tupOfFunctions



# def stockInfo(APIKEY3, ticker, typeOfInvestment):
    
#     link = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={APIkey}&datatype=csv"
#     df = pd.read_csv(link)
    
    
#     try:
#         if df[df["symbol"] == ticker] & df[df["type"] == typeOfInvestment]:
#             return "The stock ticker exists! "
#         else:
#             return "The ticker, country, or type of investment you entered does not exist in our database. Please check for incorrect spelling or spaces. Refer to the help command for any doubts."
        
#     except:
#         return "You have used the stockInfo function too many times. Please try again later. "



# def speakToCody():
#     while True:

#         userMessage = userSpeech()

#         if "search" and "local" and "file" in userMessage:
#             LocalFileCalling()

#         if userMessage:

#             if any(statement in userMessage.lower() for statement in listOfExitWords()):
#                 convo.send_message(userMessage)
#                 print("Cody: " + convo.last.text)
#                 callTts(convo.last.text)
#                 return "Success"
#                 break

#             convo.send_message(userMessage)
#             print("Cody: " + convo.last.text)
#             callTts(convo.last.text)


#         else:

#             print("Cody: No valid input received :( ")
#             callTts("No valid input received :( ")



# def callTts(message):
#     tts = pyttsx3.init()
#     # tts.setProperty('rate', 75)
#     voice = tts.getProperty("voices")
#     tts.setProperty("voice", voice[0].id)
#     tts.say(message)
#     tts.runAndWait()



# def LocalFileCalling():
#     current_directory = Path.cwd()
#     print("Current Directory:", current_directory)
#     print("\n")
#     # the root tells us the current directory, dirs will list the directories in this directory, and the files will list the files in the directory
#     file_found = False  # keeps track of if file is found or not
#     st.write("Caps matter, type the name and the filetype ex:(bot.py)")
#     name = input("Enter filename): ", )  # Add chatinput feature so that user can type that filename within streamlit

#     for root, dirs, files in os.walk(f"{current_directory}"):

#         for files in files:

#             if files.endswith(name):
#                 return "FOUND THE FILE: " + files
#                 file_found = True

#     if file_found == False:
#         return "File not found"



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

    chat = st.chat_input("Chat with Cody: ")

    if chat:
        
        if chat.lower() == "clear".lower():
            
            st.session_state["History"] = []
            return
          
        answer = GeminiAPI().genAiModel(chat, APIKEY)
        
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


# Main function automatically installs all the modules/packages from the requirements document and utilizes the API keys to call other functions
def main():
    
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    print("\n Downloaded the required directories \n")
    
    # Load API keys and retrieve API key for Gemini API
    load_dotenv()
    APIKEY = os.getenv("APIKEY")
    deployToSt(APIKEY)
    
    # API key for Weather API
    # APIKEY2 = os.getenv("APIKEY2")
    # weatherStack(APIKEY2)
    
    # # API key for Alpha Vantage API
    # APIKEY3 = os.getenv("APIKEY3")
    # alphaVantage(APIKEY3)


# Calls the main function
if __name__ == "__main__":
    main()