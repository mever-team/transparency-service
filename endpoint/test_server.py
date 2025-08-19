# clone and run
# > pip install package
# > python -m endpoint.test_server
# examples in tests/server.py (also contains full structure of a model card)
#
# server specs in http://127.0.0.1:5000/docs
# refer to the implementation in package/service/server.py
# The delay below is for how many seconds the test agent will
# pretend to be thinking, so that invalid requests can be tested.

from aicard.service import serve, TestAssistant
from threading import Thread

app, gc = serve("/apidocs", {"tassist": TestAssistant(delay=5)})

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    app.run(threaded=False)  # TODO: temporary measure for development
