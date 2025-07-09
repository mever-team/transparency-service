import os
from flask import Flask, render_template, request, jsonify, session
import modelcard
from argparse import Namespace
import uuid

from types import SimpleNamespace

from .editor import edit_mc
from .inits import init
from .templates_manager import get_templates

from .globals import globals

app = Flask(__name__)

app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config["SESSION_PERMANENT"] = False


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

import shutil
from datetime import datetime, timedelta


def cleanup_old_user_dirs(base_path="./UI/templates/sessions", max_age_minutes=60):
    now = datetime.utcnow()
    for session_id in os.listdir(base_path):
        path = os.path.join(base_path, session_id)
        if os.path.isdir(path):
            last_modified = datetime.utcfromtimestamp(os.path.getmtime(path))
            if now - last_modified > timedelta(minutes=max_age_minutes):
                shutil.rmtree(path)
                globals.pop(session_id, None)


# give id to each session
@app.before_request
def ensure_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    print(session["session_id"])
    cleanup_old_user_dirs()


@app.route("/ydata")
def ydata():
    session_id = session.get("session_id")
    return render_template(f"sessions/{session_id}/ydata.html")


@app.route("/ydata_train")
def ydata_train():
    session_id = session.get("session_id")
    return render_template(f"sessions/{session_id}/ydata_train.html")


@app.route("/ydata_eval")
def ydata_eval():
    session_id = session.get("session_id")
    return render_template(f"sessions/{session_id}/ydata_eval.html")


# Route for the main page
@app.route("/")
def index():
    # reset on session
    session.permanent = False
    force_reset = request.args.get("reset") == "1"
    if (
        force_reset
        or not session.get("has_reset")
        or not os.path.exists(
            os.path.join("./UI/templates/sessions", session["session_id"])
        )
    ):
        init(session["session_id"])
        session["has_reset"] = True

    # Default templates for left and right panes
    left_src = request.args.get("left_src", "default/welcome.html")
    right_src = request.args.get("right_src", "default/welcome_menu.html")
    return render_template("default/main.html", left_src=left_src, right_src=right_src)


# Route to handle template changes based on button click
@app.route("/change_templates", methods=["POST"])
def change_templates():
    cleanup_old_user_dirs()
    session_id = session.get("session_id")
    session_templates_path = os.path.join("./UI/templates/sessions", session_id)

    form_data = request.json.get("formData", {})
    args = SimpleNamespace()
    args.field = form_data.get("field")
    args.textarea = form_data.get("textarea")
    args.user_input = form_data.get("user_input")
    args.button = request.json.get("button")

    edit_mc(args, session_id)
    left_template, right_template = get_templates(args, session_id)

    if args.button == "Save":
        globals[session_id].mc.save(f"{session_templates_path}/model_card")
        globals[session_id].mcwithtips.save(
            f"{session_templates_path}/model_card_with_tips"
        )
        globals[session_id].mcsimplified.save(
            f"{session_templates_path}/model_card_simplified"
        )
    elif args.button == "Save and Commit":
        globals[session_id].mc.save(f"{session_templates_path}/model_card")
        globals[session_id].mcwithtips.save(
            f"{session_templates_path}/model_card_with_tips"
        )
        globals[session_id].mcsimplified.save(
            f"{session_templates_path}/model_card_simplified"
        )
        globals[session_id].mc.save(f"{session_templates_path}/~model_card")
        globals[session_id].mc.commit(session_templates_path)

    # Return the new templates and data to the front-end
    return jsonify(
        {
            "new_left_html": left_template,
            "new_right_html": right_template,
        }
    )


@app.route("/upload", methods=["POST"])
def upload():
    session_id = session.get("session_id")
    if "file" not in request.files:
        print("No file part", 400)
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        print("No selected file", 400)
        return "No selected file", 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    print(f"File uploaded successfully to {filepath}")

    button = request.form.get("button")
    field = request.form.get("field")
    file_path = filepath
    args = Namespace(button=button, field=field, file_path=file_path)
    edit_mc(args, session_id)
    left_template, right_template = get_templates(args, session_id)

    return jsonify(
        {
            "new_left_html": left_template,
            "new_right_html": right_template,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
