from flask import Flask, render_templates
app = Flask(__name__)


@app.route('/')
def hello():
#    return render_template('index.html')
    return "Hello World!"
