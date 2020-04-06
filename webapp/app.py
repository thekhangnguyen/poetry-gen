from flask import Flask, request, render_template
import os
import sys

path = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.insert(1, path)

from gpt2.interactive_conditional_samples import interact_model

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def generate():
    rhyme = str(request.form['rhyme'])
    sent = str(request.form['sentiment'])
    time = str(request.form['time-epoch'])

    seed = "<|startoftext|> [" + rhyme + ", " + sent + ", " + time + ", 4]"
    poem_txt = interact_model(input=seed, length=len(rhyme) * 45)
    poem_txt = poem_txt[:poem_txt.find("<|endoftext|>")]
    poem = poem_txt.replace("\n", "<br>")
    time = time + " century"

    return render_template('index.html', rhyme=rhyme, sent=sent, time=time, output=poem, display=True)


if __name__ == "__main__":
    app.run()
