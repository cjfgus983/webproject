from flask import Flask
app = Flask(__name__)#파이보가 들어감

@app.route('/')
def hello_pybo():
    return 'Hello, Pybo!'

app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))

import os
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')