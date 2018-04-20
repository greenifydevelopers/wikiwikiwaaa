# Feature tests.
from wiki.web.routes import convertODT
from wiki.web.routes import onePDF
from wiki.web.routes import makeUser
from wiki.web.routes import convertPDF
from wiki.web.user import UserManager
import os
from flask import Flask

app = Flask(__name__)

# Feature 1 - md to odt
# Convert the sample markdown file to an odt file.
with app.app_context():
    convertODT('test')

# Store the location where the converted file should be stored.
filename = "content/createdodts/test.odt"

# Check if the file was converted.

if os.path.exists(filename):
    print("Pass - feature 1 - md to odt")
else:
    print("Fail - feature 1 - md to odt")


# Feature 2 - Full wiki to PDF
# Convert the full wiki to one PDF.
with app.app_context():
    onePDF('test')

# Store the location where the converted file should be stored.
filename = "content/createdpdfs/fullWiki.pdf"

# Check if the file was converted.

if os.path.exists(filename):
    print("Pass - feature 2 - wiki to pdf")
else:
    print("Fail - feature 2 - wiki to pdf")


# Feature 3 - Create new user
# Create a new wiki user.
with app.app_context():
    makeUser()

# Set up UserManager to check list of users.
with app.app_context():
    newUser = UserManager('user')
    user = newUser.get_user('test')

# Check if the test user exists.
if user is not None:
    print("Pass - feature 3 - user creation")
else:
    print("Fail - feature 3 - user creation")


# Feature 4 - Create PDF and email
# Convert the current page to a PDF and email it.
with app.app_context():
    convertPDF('test')

# Store the location where the converted file should be stored.
filename = "content/createdpdfs/test.pdf"

# Check if the file was converted.
if os.path.exists(filename):
    print("Pass - feature 4 - md to pdf")
else:
    print("Fail - feature 4 - md to pdf")

# Not currently being tested: the sending of the email.
