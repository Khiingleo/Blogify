from flask import (Blueprint, render_template, url_for, flash, redirect,
                   request, abort, jsonify)
from flask_login import current_user, login_required
from blogify import db
from blogify.models import Post, Like, Comment
from blogify.posts.forms import PostForm, CommentForm
"""Handles all forms of posts routes on the blogify app"""



posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=["GET", "POST"])
@login_required
def new_post():
    """Handles the creation of new posts"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route('/post/<int:post_id>', methods=["GET", "POST"])
def post(post_id):
    """handles the viewing of a particular post based
    on it's id"""
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, form=form)


@posts.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    """Handles the updating of a post based on its id
    requires the user to be the one who posted it"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
    """Deletes a post based on it's id"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/create-comment/<int:post_id>", methods=["GET", "POST"])
@login_required
def create_comment(post_id):
    """Creates a comment based on a post id"""
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('posts.post', post_id=post_id))

@posts.route("/like-post/<int:post_id>", methods=["POST"])
@login_required
def like(post_id):
    """Like a post"""
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(author=current_user, post_id=post_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return jsonify({"likes": len(post.likes), "liked": current_user in map(lambda x: x.author, post.likes)})