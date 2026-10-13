import os
import threading
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from aicard.card.model_card import ModelCard
from aicard.service.assistants.matcher import SemanticMatcher
from aicard.service.logger import Logger
from aicard.service.converters import dict2dynamic

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(ROOT_DIR, "original_web_pages")
GPT_REORGANIZE_DIR = os.path.join(ROOT_DIR, "gpt_reorganize")
OUTPUT_DIR = os.path.join(ROOT_DIR, "matcher_output")
LOCAL_SOURCE = False
os.environ["EVALUATION_RUN"] = "1"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chdir(HTML_DIR)

# serve data markdowns through localhost so that the matcher can retrieve them as web resources
server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever, daemon=True)
server_thread.start()

# find data
logger = Logger()
data = []
for filename in sorted(os.listdir(GPT_REORGANIZE_DIR)):
    if not filename.endswith(".json"): continue
    html_filename = filename[:-4] + "html" if LOCAL_SOURCE else filename[:-5].replace('@', '/')
    data.append({ "url": f"http://huggingface.co/{html_filename}", "id": len(data) })

# recreate model cards
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0,
    fuzzer_weight=0.25,
    promote_filling_simple_fields=0.1)
matcher.start(logger)
for item_num, item in enumerate(data):
    if LOCAL_SOURCE:
        filename = os.path.basename(item["url"])
        output_filename = os.path.splitext(filename)[0] + ".json"
    else:
        filename = item["url"]
        parts = os.path.normpath(filename).split(os.sep)
        output_filename = os.path.splitext("@".join(parts[-2:]))[0] + ".json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    logger.info(f"Processing file {item_num+1}/{len(data)}: {filename}")

    md = ModelCard()
    matcher.complete(md, item["id"], item, logger,[""], job_tracker=None)
    result = dict2dynamic(md.data, {"title"})
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    logger.ok(f"Saved: {output_path}")
server.shutdown()