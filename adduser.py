import argparse
from wiki.web.user import UserManager
from flask import Flask

app = Flask(__name__)


def makeUser(username, password):
    new = UserManager('user')
    new.add_user(username, password)


parser = argparse.ArgumentParser(description='Add new user.')
parser.add_argument('username', metavar='username', type=str, nargs=1,
                    help='new username')
parser.add_argument('password', metavar='password', type=str, nargs=1,
                    help='new password')
parser.add_argument('--create', dest='create', action='store_const',
                    const=makeUser, default=makeUser,
                    help='Add new user')

args = parser.parse_args()

with app.app_context():
    args.create(args.username[0], args.password[0])

