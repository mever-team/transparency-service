import os
from flask import Flask, render_template, request, jsonify
import transparency_service
from argparse import Namespace

from types import SimpleNamespace

from .editor import edit_mc
from .inits import init
from .templates_manager import get_templates

from . import globals

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
init()


# Route for the main page
@app.route('/')
def index():
    # Default templates for left and right panes
    left_src = request.args.get('left_src', '~model_card.html')
    right_src = request.args.get('right_src', 'menu.html')
    return render_template('main.html',left_src=left_src,right_src=right_src)


# Route to handle template changes based on button click
@app.route('/change_templates', methods=['POST'])
def change_templates():
    form_data = request.json.get('formData', {})
    args = SimpleNamespace()
    args.field = form_data.get('field')
    args.textarea = form_data.get('textarea')
    args.user_input = form_data.get('user_input')
    args.button = request.json.get('button')

    edit_mc(args)
    left_template, right_template = get_templates(args)

    if args.button == "Save":
        globals.mc.save('model_card')
        globals.mcwithtips.save('model_card_with_tips')
        globals.mcsimplified.save('model_card_simplified')
    elif args.button == "Save and Commit":
        globals.mc.save('model_card')
        globals.mcwithtips.save('model_card_with_tips')
        globals.mcsimplified.save('model_card_simplified')
        globals.mc.save('templates/~model_card')
        globals.mc.commit()

    # Return the new templates and data to the front-end
    return jsonify({'new_left_html': left_template,'new_right_html': right_template,})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        print('No file part', 400)
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        print('No selected file', 400)
        return 'No selected file', 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    print(f'File uploaded successfully to {filepath}')


    button = request.form.get('button')
    field = request.form.get('field')
    file_path = filepath
    args = Namespace(button=button, field=field, file_path=file_path)
    edit_mc(args)
    left_template, right_template = get_templates(args)

    return jsonify({'new_left_html': left_template,'new_right_html': right_template,})

if __name__ == '__main__':
    app.run(debug=True)
