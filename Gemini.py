import google.generativeai as genai


class GeminiAPI:
    
    # Join words in the sentence from the generated output
    def joinWordsInOutput(self, output):
    
        arr = []
        for word in output:
            arr.append(word.text)
        response = " ".join(arr)
        return response


    # Set up the model
    def generationConfig(self):
        
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192}
        return generation_config


    # Sets the settings to block explicit content
    def safetySettings(self):
        
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


    def genAiModel(self, chat, apiKey):
        
        try:
            
            genai.configure(api_key=apiKey)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config = self.generationConfig(),
                                        safety_settings = self.safetySettings())
            convo = model.start_chat(history=[])
            output = convo.send_message(chat, stream=True)

            if "search" and "local" and "file" in self.joinWordsInOutput(output):
                st.write(LocalFileCalling())
            
            return self.joinWordsInOutput(output)  

        except Exception as e:
            print(f"An error occurred {e}")
            return None