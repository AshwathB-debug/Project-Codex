# Project Codex


## Project Description
Project Codex (aka Cody) is developed to help users simplify their day-to-day tasks on their computer through the use of AI. Powered by the Gemini API, this chatbot was made with the intention to help visually impaired people to be able to speak to the chatbot and for it to act like a voice assistant that can do a multitude of tasks from presenting various information.  


## Features
1. SpeechRecognition: This project utilizes the SpeechRecognition module to be able to speak to the computer, converting spoken words into text that the Chatbot could process to provide a response.
2. API key security: The project utilizes an environment file to encrypt API keys from landing into the wrong hands.
3. Text-To-Speech: Utilizes the pyttsx3 library to convert the text response from Cody into speech. This key feature makes the Chatbot stands out from other GenAI models because it can speak to the user instead of printing the output to screen. 
4. Streamlit: Deployed our Chatbot to Streamlit to increase user engagement and productivity by 100% and making a more user-friendly tool.
5. File opener: Using the Chatbot, one of the tasks we can do is to access files within our computer using the pathlib module.


## Usage
If you'd like to run the project on your own, follow these steps:
1. Clone the repository or download the files
2. Open the terminal and type "streamlit run Chatbot.py" and it will automatically download all the required modules/libraries for you and take you to streamlit to interact with Cody.


## Learning Resources
1. Streamlit: Utilized streamlit in our project being inspired by the tutorial that shows how to deploy a Chatbot to streamlit: https://www.youtube.com/watch?v=o4ZhXSVuPyc&t=748s&ab_channel=KrishNaik