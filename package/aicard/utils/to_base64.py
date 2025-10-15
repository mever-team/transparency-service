import base64
import os
import urllib.request

import validators

def to_base64(content):
    try:
        decoded = base64.b64decode(content, validate=True)
        if decoded:
            return content
    except Exception:
        pass

    if validators.url(content):
        with urllib.request.urlopen(content) as response:
            data = response.read()
            encoded = base64.b64encode(data).decode("utf-8")
            return encoded

    assert os.path.isfile(content), "File not found."
    with open(content, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode("utf-8")
    return encoded
