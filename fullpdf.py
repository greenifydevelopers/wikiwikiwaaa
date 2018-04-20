import argparse
from wiki.web.routes import onePDF
from flask import Flask

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Convert full Wiki to PDF.')
parser.add_argument('wiki', metavar='wiki', type=str, nargs=1,
                    help='an integer for the accumulator')
parser.add_argument('--convert', dest='converter', action='store_const',
                    const=onePDF, default=onePDF,
                    help='Convert full Wiki to PDF')

args = parser.parse_args()
with app.app_context():
    print(args.converter(args.wiki[0]))
