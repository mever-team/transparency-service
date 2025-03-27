from flask import Flask, render_template, request, jsonify
import transparency_service

import tkinter as tk
from tkinter import filedialog

import pandas as pd

from types import SimpleNamespace

from editor import edit_mc
from inits import init
from templates_manager import get_templates
import globals

app = Flask(__name__)
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
    elif args.button == "Save and Commit":
        globals.mc.save('model_card')
        globals.mc.save('templates/~model_card')
        globals.mc.commit()

    # Return the new templates and data to the front-end
    return jsonify({'new_left_html': left_template,'new_right_html': right_template,})

if __name__ == '__main__':
    app.run(debug=True)
