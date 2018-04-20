from flask import Flask
import os
from wiki.web import create_app

app = Flask(__name__)

directory = os.getcwd()
app = create_app(directory)


if __name__ == '__main__':
    app.run(debug=True)
