# clone and run
# > pip install package
# > python -m ui.test_server
# examples in tests/server.py (also contains full structure of a model card)
#
# .venv serves index.html at http://127.0.0.1:5000
# server specs in http://127.0.0.1:5000/apidocs
# refer to the implementation in package/service/server.py
# The delay below is for how many seconds the test agent will
# pretend to be thinking, so that invalid requests can be tested.

from aicard.service import serve
from aicard.service.assistants import SemanticMatcher, Prompter, Combined
from aicard.agents import Ollama
from threading import Thread
from aicard.agents.extensions.embeddings import ImageClassifier

def preprocessor(text: str) -> str:
    #print("preprocessing text size "+str(len(text)))
    for symbol in "()[]*_/\\\"'`:;-+.,?\n\t\r=|><{}&!#": # remove common symbols
        text = text.replace(symbol, " ")
    text = text.lower()
    found = dict()
    result = ""
    pos = 0
    window = float('inf') # after every set number of words allow repetition (large number to disable)
    for t in text.split(" "):
        pos += 1
        # convert to a set while preserving order to keep phrases
        if not t: continue
        prev_pos = found.get(t, None)
        found[t] = pos # do this here to preserve continuity of concepts
        if prev_pos and prev_pos>pos-window: continue
        result += " "+t
    result = "Respond with full sentences. Do not mention missing information. Here are keywords describing the model: "+result
    #print("reduced to size "+str(len(result)))
    return result


image_classifier = None# ImageClassifier()
app, gc = serve({
        "agent": Combined(
            complete=SemanticMatcher(external_get_timeout_sec=3),
            refine=Prompter(
                Ollama("llama3.2:latest", name="🦙 Llama 3.2", timeout_secs=60),
                description="Llama 3.2 is used as the base model.",
                #image_classifier=image_classifier,
                text_preprocessor=preprocessor),
        )
    },
    env="ui/.env",
)

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    app.run(threaded=False)  # TODO: temporary measure
