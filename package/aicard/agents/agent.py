class Agent:
    def _run(self, content: str, task: str, output_format:str | None = None): raise NotImplementedError("This is an abstract agent class")
    def summarization(self, content: str): return self._run(content, task="summarization")
    def simplification(self, content: str): return self._run(content, task="simplification")
    def completion(self, content: str, output_format:str | None): return self._run(content, task="completion", output_format=output_format)
    def hint(self, content: str): return self._run(content, task="hint")
