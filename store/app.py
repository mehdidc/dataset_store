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
    return get_path('/')


@app.route('/<path:path>')
def get_path(path):
    abs_path = config.dirname + "/" + path
    if os.path.isdir(abs_path):
        if not path.endswith("/"):
            path += "/"

        filenames = os.listdir(abs_path)
        filenames = sorted(filenames, key=os.path.isdir)
        filenames = filter(file_pattern.search,
                           filenames)

        def get_url(filename):
            abs_path_filename = abs_path + "/" + filename
            link = path + filename
            print(link)
            if os.path.isdir(abs_path_filename):
                name = filename + "/"
            else:
                name = filename
            return Url(name=name, link=link)
        urls = map(get_url, filenames)
        return render_template("index.html", urls=urls)
    else:
        return get_filename(abs_path)


def get_filename(filename):
    if not os.path.exists(filename):
        return "404 - {} not found".format(filename), 404
    else:
        return send_file(filename)


@app.route('/stores')
def stores():
    return jsonify(mirrors=get_mirrors())
