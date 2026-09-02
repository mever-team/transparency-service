import anthropic
import os
from string import Template
import json
from aicard.agents.agent import Agent


class Claude(Agent):
    tasks = {
        "simplification": "You are a helpful assistant that summarizes documents.",
        "completion": Template("provide a model card based on $info. Do not use any other information other than that.")
    }

    def __init__(self, 
                #  model='claude-sonnet-5', 
                 model='claude-fable-5', 
                 name=None, 
                 max_tokens=4*4096,
                 timeout_secs=60):  # pragma: no cover
        self._model = model
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        anthropic_workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")
        assert anthropic_api_key, "Can't find ANTHROPIC_API_KEY in the environment."
        assert anthropic_workspace_id, "Can't find ANTHROPIC_WORKSPACE_ID in the environment."
        self.client = anthropic.Anthropic(default_headers={"anthropic-workspace-id": os.getenv("ANTHROPIC_WORKSPACE_ID")})
        self.max_tokens = max_tokens

    def _run(self, content: str, task: str, **params):  # pragma: no cover
        assert isinstance(content, str), "content must be of type str"
        assert task in Claude.tasks, "Not supported task: " + task
        config = {"effort": "medium"}
        if params:
            config.update(params)
        response = self.client.messages.create(
            model=self._model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": Claude.tasks[task].substitute(info=content)}],
            output_config=config,
        )
        result = "".join(block.text for block in response.content if block.type == "text")
        return result
