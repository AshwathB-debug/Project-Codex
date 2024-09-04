import speech_recognition as sr
import google.generativeai as genai
import webbrowser
import os
from dotenv import load_dotenv
import pyttsx3
import streamlit



def userSpeech(): 
  
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak to Cody: ")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

        try:
            audio = recognizer.listen(source, timeout=5)  # Set the timeout to 5 seconds
            message = recognizer.recognize_google(audio)
            #print(f"You said: {message}")
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



def speakToCody():

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config, safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    
    
    while True:
       
      userMessage = userSpeech()
      
      if userMessage:
        
        if "Google" in userMessage:
          webbrowser.open('http://www.google.com')
        
        
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



def listOfExitWords():
  
    exitStatements = ["bye", "goodbye", "see ya", "that's it for today"]
    return exitStatements
    

def callTts(message):
    tts = pyttsx3.init()
    # tts.setProperty('rate', 75)
    voice = tts.getProperty("voices")
    tts.setProperty("voice", voice[0].id)
    tts.say(message)
    tts.runAndWait()



def getApiKey():
  
    load_dotenv()
    APIKEY = os.getenv("APIKEY")
    return APIKEY



if __name__ == "__main__":
  
    
    genai.configure(api_key=getApiKey()) # REMEMBER TO MAKE A ENCRYPTED FILE TO SECURE API KEY
    
    # Set up the model
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 0,
      "max_output_tokens": 8192,
    }

    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
    ]
    
    print(speakToCody())