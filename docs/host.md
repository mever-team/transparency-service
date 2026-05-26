# Host a local server

If you have *aicard* installed, you can immediately self-host a server.
To do so, create a dictionary of assistants and start a flask service. 
This will set up everything the first time, including a database. 
If you do not plan to expose the server externally, you can login with
the default administrator credentials, like above.
If you want console instead of persistent logging, skip any logger setup. 
Do note that, if an `.env` file is provided, then 
there will be an attempt to retrieve missing arguments from there.
Below is an example service whose assistant is primarily used for testing:

```python
from aicard.service import serve, TestAssistant
from threading import Thread

app, gc = serve({"tassist": TestAssistant(delay=5)}, env=".env")
Thread(target=gc, daemon=True).start()  # needed for long uptimes
app.run(threaded=False)  # current version requires single-threaded run
```

```bash
# .env
INDEX=/apidocs # redirect_index
USER=admin  # admin_username 
PASS=admin  # admin_password
LOG=log.txt # log_file
```

**Garbage collection (gc)** is a callback function that periodically cleans
up resources that are *estimated* as to no longer be in use. This includes 
cleanup of the card access cache and expired tokens. Creating a thread for running 
the `gc` function is required for servers with long uptimes to avoid memory bloat.
However, you can skip spawning a thread for this if host a shorter-time server 
for managing only your own experiments.