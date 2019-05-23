from flask import Flask
from flask import request
import os
from spell_checker import get_spell_check
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Spell Corrector!"


@app.route("/spellCorrect/<input_text>")
def execute_get_spell_check(input_text):
    try:
        print(input_text)
        output = get_spell_check(input_text)
        #return '{}\n'.format(extracted_data)  
        print("result: ", output)
        return output
    except Exception as e:
        print(e)


if __name__ == '__main__':
    host = os.environ.get('IP', '0.0.0.0')
    app.run(host=host, port=8080, debug=True)
