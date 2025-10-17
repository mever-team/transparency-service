import base64
import os
import urllib.request

import validators

def to_base64(content):
    try:
        decoded = base64.b64decode(content, validate=True)
        if decoded:
            return content, 200
    except Exception:
        pass

    if validators.url(content):
        try:
            with urllib.request.urlopen(content) as response:
                content_type = response.info().get_content_type()
                allowed_types = ["image/jpeg", "image/png", "image/webp", "image/bmp"]
                if content_type not in allowed_types:
                    return content, 415
                data = response.read()
                encoded = base64.b64encode(data).decode("utf-8")
                return encoded, 200
        except Exception:
            return content, 500

    if not os.path.isfile(content):
        return content, 500
    try:
        with open(content, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode("utf-8")
        return encoded, 200
    except Exception:
        return content, 500
