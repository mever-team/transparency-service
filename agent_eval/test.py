import os
import threading
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from aicard.card.model_card import ModelCard
from aicard.service.assistants.matcher import SemanticMatcher
from aicard.service.logger import Logger
from aicard.service.jobs_tracker import CardJobsTracker
from aicard.service.converters import dict2dynamic


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(ROOT_DIR, "original_web_pages")
GPT_REORGANIZE_DIR = os.path.join(ROOT_DIR, "gpt_reorganize")
OUTPUT_DIR = os.path.join(ROOT_DIR, "matcher_output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# --------------------------------------------------
# Serve the markdown files
# --------------------------------------------------

os.chdir(HTML_DIR)

server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
server_thread = threading.Thread(
    target=server.serve_forever,
    daemon=True
)
server_thread.start()

print("Serving html files at http://localhost:8000/")


# --------------------------------------------------
# Create data list from gpt_reorganize
# --------------------------------------------------

data = []

for filename in sorted(os.listdir(GPT_REORGANIZE_DIR)):
    if filename.endswith(".json"):
        html_filename = filename[:-4] + "html"

        data.append({
            "url": f"http://localhost:8000/{html_filename}",
            "id": len(data)
        })

print(f"Found {len(data)} files to process.")


# --------------------------------------------------
# Start matcher
# --------------------------------------------------

logger = Logger()
job_tracker = CardJobsTracker()

matcher = SemanticMatcher()
matcher.start(logger)


# --------------------------------------------------
# Process each file
# --------------------------------------------------

for item in data:

    filename = os.path.basename(item["url"])
    output_filename = os.path.splitext(filename)[0] + ".json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    print(f"Processing: {filename}")

    # Create a fresh model card for every file
    md = ModelCard()

    matcher.complete(
        md,
        item["id"],
        item,
        logger,
        [""],
        job_tracker
    )

    result = dict2dynamic(md.data, {"title"})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Saved: {output_path}")


# --------------------------------------------------
# Shutdown server
# --------------------------------------------------

server.shutdown()

print("Done.")