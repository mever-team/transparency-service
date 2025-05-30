from UI.app import app, cleanup_old_user_dirs

import threading
import time

def start_cleanup_loop():
    def loop():
        while True:
            cleanup_old_user_dirs()  # your cleanup function
            time.sleep(60)  # every 60 seconds

    t = threading.Thread(target=loop, daemon=True)
    t.start()

if __name__ == "__main__":
    start_cleanup_loop()
    app.run()