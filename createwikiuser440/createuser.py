from wiki.web.forms import NewUserForm
from wiki.web.user import UserManager

def user_create():
    form = NewUserForm()
    return render_template('createuser.html', form=form)


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
