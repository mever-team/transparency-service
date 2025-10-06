class Agent:
    def _run(self, content: str, task: str, params:dict | None): raise NotImplementedError("This is an abstract agent class")
    def summarization(self, content: str, params:dict | None = None): return self._run(content, task="summarization", params=params)
    def simplification(self, content: str, params:dict | None = None): return self._run(content, task="simplification", params=params)
    def completion(self, content: str, params:str | None = None): return self._run(content, task="completion", params=params)
    def hint(self, content: str, params:dict | None = None): return self._run(content, task="hint", params=params)
