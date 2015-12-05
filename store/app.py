import os
import config
import re
from collections import namedtuple
from flask import Flask, render_template, send_file, jsonify
from tasks import get_mirrors

app = Flask(__name__)
app.debug = True

file_pattern = re.compile(config.pattern)

Url = namedtuple('Url', ['name', 'link'])


@app.route('/')
def index():
    filenames = filter(file_pattern.search,
                       os.listdir(config.dirname))
    urls = map(lambda filename: Url(name=filename, link=filename),
               filenames)
    return render_template("index.html", urls=urls)


@app.route('/stores')
def stores():
    return jsonify(mirrors=get_mirrors())


@app.route('/<filename>')
def get_filename(filename):
    filename = os.path.join(config.dirname, filename)
    if not os.path.exists(filename):
        return "404 - {} not found".format(filename), 404
    else:
        return send_file(filename)
