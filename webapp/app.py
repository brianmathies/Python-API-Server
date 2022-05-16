from flask import Flask
from datetime import datetime
from flask import request, jsonify, Response
import os
import base64
import json
import random
from types import SimpleNamespace
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return "API Server"

@app.route("/pronounce-it-right/phonemes", methods=['POST'])
def post():
# decode base64 string to original binary sound object
    b64 = request.get_data()

    x = json.loads(b64, object_hook=lambda d: SimpleNamespace(**d))
    b64_text = str(x.payload)
    # print(b64_text)
    decodedData = base64.b64decode(b64_text)
    outdir = os.getcwd()

    r = int(random.random() * 1000000)
    wavfile = os.path.join(outdir, '{0}.wav'.format(r))
    phoneme_file = os.path.join(outdir, 'phonemes_{0}.txt'.format(r))
    with open(wavfile, 'wb') as file:
        file.write(decodedData)
    exe_path = 'C:\\Users\\brianmathies\\git\\allosaurus\\allosaurus\\output\\convert_phonemes\\convert_phonemes.exe'
    os.system('python -m allosaurus.run -e 1.0 -i {0} -o {1}'.format(wavfile, phoneme_file))

    phonemes = ''
    with open(phoneme_file, 'r', encoding='utf-8') as file:
        phonemes = file.read()

    response = jsonify(phonemes=phonemes.replace(' ', '').replace('\n', ''))

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True, host='10.0.0.4', port=5000, use_reloader=True)

