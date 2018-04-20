import pypandoc
from flask import send_file


def convertPDF(url):
    pypandoc.convert('content/' + url + '.md', 'pdf', outputfile='content/createdpdfs/' + url + '.pdf',
                     extra_args=['-V geometry:margin=1.5cm'])
    app = Flask(__name__)

    app.config.update(dict(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME='csc440emailer@gmail.com',
        MAIL_PASSWORD='wiki440!'
    ))

    mail = Mail(app)
    mail.init_app(app)
    msg = Message("Your PDF",
                  sender="test@example.com",
                  recipients=["csc440emailer@gmail.com"])
    msg.body = "Please find attached your PDF from WikiWikiWaaa."
    mail.send(msg)

    with app.open_resource('../../content/createdpdfs/' + url + '.pdf') as fp:
        msg.attach("wikipage.pdf", "application/pdf", fp.read())

    try:
        return send_file('../../content/createdpdfs/' + url + '.pdf')
    except IOError:
        pass