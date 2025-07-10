import os
import requests
import json


class Ollama_Prompts:
    """Container class for all system prompts."""

    def __init__(self):
        # TODO: write the prompts here or read them from a file
        object.__setattr__(self, "summarization", "ollamaYou are a helpful assistant that summarizes documents.")
        object.__setattr__(self, "json_completion", "ollamaYou are a helpful assistant completes json fields of a model card.")

    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot modify prompts")


class Ollama_Agent:
    def __init__(self, model = 'llama3.2:3b'):
        # Set model to any available model you have in your Ollama service
        object.__setattr__(self, "OLLAMA_BASE_URL", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
        object.__setattr__(self, "ollama_url", f"{self.OLLAMA_BASE_URL}/api/chat")
        object.__setattr__(self, "prompt", Ollama_Prompts())

        data = {"model": model, "messages": [{"role": "user", "content": "Request test"}], "stream": False,}
        response = requests.post(self.ollama_url, json=data)
        assert response.status_code == 200, f"Response Text: {response.text}\nFailed to initialize model '{model}'."
        object.__setattr__(self,"model", model)
        # TODO: use those
        self.max_tokens = 4000
        self.temperature = 0.7
        self.top_p = 1

    def __setattr__(self, name, value):
        if name == "prompt" or name == "OLLAMA_BASE_URL" or name == "ollama_url" or name == "model": raise AttributeError("Modification not allowed.")
        super().__setattr__(name, value)

    def __call__(self, content , prompt):
        """
        Calls an Ollama model with a given system prompt and user content.

        Args:
            content (str): The user input or message to send to the Ollama model.
            prompt (str): A system-level instruction guiding how the model should behave. One of self.prompt

        Returns:
            str: The model's response as a string.
        """
        assert isinstance(content, str), "content must be of type str"
        assert prompt in vars(self.prompt).values(), "Prompt must be one of the predefined prompts"

        messages = [{"role": "system", "content": prompt,},{"role": "user", "content": content},]
        data = {"model": self.model, "messages": messages, "stream": False}
        response = requests.post(self.ollama_url, json=data)
        model_output = json.loads(response.text)["message"]["content"]
        return model_output