from flask import Blueprint, render_template, request
from blogify.models import Post
"""Blogify main routes including home and about pages"""

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    """handles the homepage route"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    """handles the about page route"""
    return render_template("about.html", title="about")