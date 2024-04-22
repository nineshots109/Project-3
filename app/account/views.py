from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from app import db
from app.account.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
)
from app.models import User

account = Blueprint('account', __name__)
main = Blueprint('main', __name__)


@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/')
@main.route('/index')
def index():
    return redirect (url_for('index.html'))

@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'success')
            
    return render_template('account/login.html', form=form)

@account.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user without sending a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return render_template('account/index.html')
    return render_template('account/register.html', form=form)


#@account.route('/logout', methods=['GET', 'POST'])
#@login_required
#def logout():
#    logout_user()
#    flash('You have been logged out.', 'info')
#    # Redirect to the login page after logout
#    return render_template('account/index.html')
@account.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out.', 'info')
    else:
        flash('You are already logged out.', 'warning')
    # Redirect to the login page after logout or if already logged out
    return render_template('account/index.html')


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

@account.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    """Display a user's account information."""
    return render_template('account/manage.html', user=current_user, form=None)

@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    if not current_user.is_anonymous:
        return redirect('/')
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            flash('A password reset link has been sent to {}.'.format(
                form.email.data), 'warning')
            # Here, you can add the logic to send the reset link via email if needed
            return redirect(url_for('account.login'))
    return render_template('account/reset_password.html', form=form)

@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('account.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'form-error')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('account.login'))
        else:
            flash('The password reset link is invalid or has expired.', 'form-error')
            return redirect(url_for('account.login'))  # Updated to redirect to login route
    return render_template('account/reset_password.html', form=form)

@account.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'form-success')
            return redirect('/')
        else:
            flash('Original password is invalid.', 'form-error')
    return render_template('account/manage.html', form=form)

@account.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        current_user.email = new_email
        db.session.commit()
        flash('Your email address has been updated.', 'success')
        return redirect('/')
    return render_template('account.manage', form=form)

    
