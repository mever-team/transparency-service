import requests
import os
import json

class Extractor():
    def __init__(self):
        base_url: str=os.getenv("OLLAMA_BASE_URL","http://localhost:11434")
        self.__url = f"{base_url}/api/chat"
        self.__model = 'mistral:latest'
        test = requests.post(self.__url, json={
            "model": self.__model,
            "stream": False,
            "messages": [{"role": "user", "content": "Request test"}],
        })
        assert test.status_code == 200, f"Failed to initialize model '{self.__model}'\nResponse: {test.text}"
    
    def name(self, content: str):
        task="what is the name of the model?"
        payload = {
            "model": self.__model,
            "stream": False,
            "messages": [{"role": "system", "content": task}, {"role": "user", "content": content}]
        }
        format = {"format": {
            "type": "object",
                "properties": {
                    "name of the model. Give me just the name acronym": {
                        "type": "string"
                    }
                }
            }
        }
        payload.update(format)
        response = requests.post(self.__url, json=payload)
        response = json.loads(response.text)["message"]["content"]
        response = json.loads(response)
        key = next(iter(response))
        value = response[key]
        return value