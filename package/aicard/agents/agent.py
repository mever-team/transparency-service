class Agent:
    def name(self):
        return "🤖 "+self.__class__.__name__
    def _run(self, content: str, task: str, **params): raise NotImplementedError("This is an abstract agent class")
    def summarization(self, content: str, **params): return self._run(content, task="summarization", **params)
    def simplification(self, content: str, **params): return self._run(content, task="simplification", **params)
    def completion(self, content: str, **params): return self._run(content, task="completion", **params)
    def hint(self, content: str, **params): return self._run(content, task="hint", **params)
