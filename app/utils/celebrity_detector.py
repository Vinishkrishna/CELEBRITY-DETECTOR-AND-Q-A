import os
import base64 #encode your image to api request,as image can't be sent directly to api
import requests  #send your request to your API

class CelebrityDetector:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions" #api url we have to hit to get output
        self.models = "meta-llama/llama-4-maverick-17b-128e-instruct"

    def identify(self,image_bytes):
        encoded_image = base64.b64encode(image_bytes).decode() #converting bytes images to encoded image,image sending to api shoud be converted to base 64 format
        headers = {
            "Authorization" : f"Bearer {self.api_key}",#Used to pass authentication info (like API keys, JWT tokens).
            "Content-Type" : "application/json" #Tells the server what format the request body is in.
        }

        prompt = {
            "model": self.models,
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": """You are a celebrity recognition expert AI. 
Identify the person in the image. If known, respond in this format:

- **Full Name**:
- **Profession**:
- **Nationality**:
- **Famous For**:
- **Top Achievements**:

If unknown, return "Unknown".
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,    
            "max_tokens": 1024     
        }

        #max_token is limit of the size of the response when you will give the query,sot the output will be generated within 1024 tokens
        response = requests.post(self.api_url,headers=headers,json=prompt)

        if response.status_code==200: #success
            result = response.json()['choices'][0]['message']['content']
            name=self.extract_name(result)
            return result,name
        
        return "Unknown",""
    
    def extract_name(self,content):
        for line in content.splitlines():
            if line.lower().startswith("- **full name**:"):
                return line.split(":")[1].strip()
        
        return "Unknown"