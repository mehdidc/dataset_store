import os
import config
import re
from collections import namedtuple

from flask import Flask, render_template, send_file

app = Flask(__name__)
app.debug = True

file_pattern = re.compile(config.pattern)
print(file_pattern.search("filename.py"))

Url = namedtuple('Url', ['name', 'link'])


@app.route('/')
def index():
    filenames = filter(file_pattern.search,
                       os.listdir(config.dirname))
    urls = map(lambda filename: Url(name=filename, link=filename),
               filenames)
    return render_template("index.html", urls=urls)


@app.route('/<filename>')
def get_filename(filename):
    return send_file(filename)


if __name__ == "__main__":
    app.run()
