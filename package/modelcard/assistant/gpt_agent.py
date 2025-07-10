import openai
import os


class GPT_Prompts:
    """Container class for all system prompts."""

    def __init__(self):
        # TODO: write the prompts here or read them from a file
        object.__setattr__(self, "summarization", "gptYou are a helpful assistant that summarizes documents.")
        object.__setattr__(self, "json_completion", "gptYou are a helpful assistant completes json fields of a model card.")

    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot modify prompts")


class GPT_Agent:
    def __init__(self, model = 'gpt-3.5-turbo'):
        # gpt-3.5-turbo gpt-4
        openai.api_key = os.getenv("OPENAI_API_KEY")
        assert openai.api_key is not None, "Can't find OPENAI_API_KEY in the environment."
        object.__setattr__(self, "prompt", GPT_Prompts())

        object.__setattr__(self, "model", model)
        self.max_tokens = 4000
        self.temperature = 0.7
        self.top_p = 1

    def __setattr__(self, name, value):
        if name == "prompt" or name == "model" : raise AttributeError("Modification not allowed.")
        super().__setattr__(name, value)

    def __call__(self, content , prompt):
        """
        Calls the GPT model with a given system prompt and user content.

        Args:
            content (str): The user input or message to send to the GPT model.
            prompt (str): A system-level instruction guiding how the model should behave. One of self.prompt

        Returns:
            str: The model's response as a string.
        """
        assert isinstance(content, str), "content must be of type str"
        assert prompt in vars(self.prompt).values(), "Prompt must be one of the predefined prompts"

        messages = [{"role": "system", "content": prompt,},{"role": "user", "content": content},]
        response = openai.chat.completions.create(model=self.model, messages=messages, max_tokens=self.max_tokens, temperature=self.temperature, top_p=self.top_p,)
        model_output = response.choices[0].message.content
        return model_output