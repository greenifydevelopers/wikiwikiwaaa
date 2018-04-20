import argparse
from wiki.web.routes import convertPDF
from flask import Flask

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Convert md to pdf.')
parser.add_argument('md', metavar='md', type=str, nargs=1,
                    help='The markdown file to convert')
parser.add_argument('--convert', dest='converter', action='store_const',
                    const=convertPDF, default=convertPDF,
                    help='Convert markdown file to PDF')

args = parser.parse_args()
with app.app_context():
    print(args.converter(args.md[0]))
