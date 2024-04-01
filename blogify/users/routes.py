from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, login_user, logout_user, current_user
from blogify import db, bcrypt
from blogify.models import User, Post
from blogify.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                 RequestResetForm, ResetPasswordForm)
from blogify.users.utils import save_picture, send_reset_email, send_registration_email
"""
    Authentication and users routes
"""


users = Blueprint('users', __name__)


@users.route('/register', methods={"GET", "POST"})
def register():
    """Registeration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        send_registration_email(user)
        flash(f'Your account has been created! please check your mail to confirm registration', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/confirm_registration/<token>", methods=["GET", "POST"])
def confirm_registration(token):
    user = User.verify_reset_token(token)
    if user:
        user.confirmed = True
        db.session.commit()
        flash('Registration confirmed successfully! You can now log in.', 'success')
        return redirect(url_for('users.login'))
    else:
        flash('Invalid or expired token. Please try registering again.', 'danger')
        return redirect(url_for('users.register'))


@users.route('/login', methods=["GET", "POST"])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.confirmed:
                login_user(user, remember=form.remember.data)
                next_page= request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash("Please confirm your registration before logging in.", 'warning')
        else:
            flash("Log in unsuccessful, please check email and password", 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """User account's route"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    """User's posts route"""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """Reset password request route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("a token a has been sent to your email", 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Reset password token route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid Token or Token Has Expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f"Your Password has been updated, You can now Log in!", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)