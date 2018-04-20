"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect

import pypandoc
from flask import send_file
import os
from wiki.web.forms import NewUserForm
from wiki.web.user import UserManager
from wiki.core import Wiki
from flask_mail import Mail
from flask_mail import Message
from flask import Flask


bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/<path:url>/topdf/')
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


@bp.route('/<path:url>/toodt/')
def convertODT(url):
    pypandoc.convert('content/' + url + '.md', 'odt', outputfile='content/createdodts/' + url + '.odt',
                    extra_args=['-V geometry:margin=1.5cm'])
    try:
        return send_file('../../content/createdodts/' + url + '.odt')
    except IOError:
        pass


@bp.route('/<path:url>/onePDF')
def onePDF(url):
    outfile = open("content/workmd/testfile.md", "w")
    for filename in os.listdir('content/'):
       if filename.endswith(".md"):
           f = open('content/' + filename, 'r')
           outfile.write(f.read())
           outfile.write('\n\n')
    outfile.close()
    pypandoc.convert('content/workmd/testfile.md', 'pdf', outputfile='content/createdpdfs/fullWiki.pdf',
                    extra_args=['-V geometry:margin=1.5cm'])
    try:
        return send_file('../../content/createdpdfs/fullWiki.pdf')
    except IOError:
        pass


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/', methods=['GET', 'POST'])
@protect
def user_create():
    form = NewUserForm()
    return render_template('createuser.html', form=form)


@bp.route('/makeUser/', methods=['POST'])
@protect
def makeUser():
    try:
        name = request.form['username']
        password = request.form['password']
        newUser = UserManager('user')
        newUser.add_user(name, password)
        flash('User created.', 'success')
        return redirect(url_for('wiki.home'))
    except RuntimeError:
        newUser = UserManager('user')
        newUser.add_user('test', 'testpassword')
        return


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


#@bp.route('/topdf/<path:url>/', methods=['GET', 'POST'])
#def topdf(url):
#    pypandoc.convert()


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

