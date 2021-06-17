import functools
import re

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash


""" This creates a Blueprint named 'auth'. Like the application object, the blueprint needs to know where it’s defined, 
so __name__ is passed as the second argument. The url_prefix will be prepended to all the URLs associated with
the blueprint. """
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        """ elif <Validate that username is not already registered by querying the database and checking if a result is returned> """

        if error is None:
            """ url_for() generates the URL for the login view based on its name """
            """ redirect() generates a redirect response to the generated URL """
            return redirect(url_for('auth.login'))
        """ flash() stores messages that can be retrieved when rendering the template. """
        flash(error)

    """  render_template() will render a template containing the HTML """
    return render_template('auth/register.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        """         user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() """
        error = None

        if username is None:
            error = 'Username is empty'
        elif not check_password_hash(user['password'], password) is None:
            """ check_password_hash() hashes the submitted password in the same way as the stored hash and securely compares them. 
            If they match, the password is valid """
            error = 'Password is incorrect'

        if error is None:
            """ session is a dict that stores data across requests """
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    """ else
            g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()  """


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
