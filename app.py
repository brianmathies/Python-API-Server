from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    return "API Server"

if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)

