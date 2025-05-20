from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

MESSAGES_FILE = 'messages.json'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']

        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r') as f:
                messages = json.load(f)
        else:
            messages = []

        messages.append({'username': username, 'message': message})

        with open(MESSAGES_FILE, 'w') as f:
            json.dump(messages, f)

        return redirect(url_for('index'))

    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as f:
            messages = json.load(f)
    else:
        messages = []

    return render_template('index.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)