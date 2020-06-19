from datetime import datetime
from flask import render_template, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from markupsafe import escape
from sqlalchemy.sql import text
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post


@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET'])
def index():
    # get the title and first image of the most recent post
    return render_template('index.html', title='index page')

@bp.route('/path/<path:subpath>/', methods=['GET'])
def subpath_test(subpath):
    # get the title and first image of the most recent post
    return 'Subpath %s' % subpath


@bp.route('/posts/', methods=['GET', 'POST'])
def posts():
    if request.args:
        if request.args.get('tag'):
            posts = Post.query.filter_by(tag=request.args.get('tag'))
            message = "{} post{} found".format(posts.count(), "" if posts.count() == 1 else "s")
        elif request.args.get('user_id'):
            posts = Post.query.filter_by(user_id=request.args.get('user_id'))
            message = "{} post{} found".format(posts.count(), "" if posts.count() == 1 else "s")
        else:
            posts = Post.query.all()
            message = "not found"
    else:
        posts = Post.query.all()
        message = None
    return render_template('posts.html', posts=posts, message=message)

@bp.route('/posts/new/', methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', post_id=post.id)) #want to go to the post, need the id
    return render_template('_post.html', form=form, post=None)


@bp.route('/posts/<post_id>/', methods=['GET'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post)

@bp.route('/posts/<post_id>/edit/', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('_post.html', form=form, post=post)

@bp.route('/posts/<int:post_id>/delete/', methods=['DELETE'])
@login_required
def post_destroy(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post:
        # Post.query.filter_by(id=post_id).delete()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))

@bp.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/user/<username>/edit/', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.profile = form.profile.data
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.profile.data = current_user.profile
    return render_template('_user.html', form=form)


@bp.route('/users/', methods=['GET', 'POST'])
@login_required
def users():
    if request.args:
        if request.args.get('following'):
            users = User.query.filter_by(username=request.args.get('following')).first().followed
            message = "{} user{} found".format(users.count(), "" if users.count() == 1 else "s")
        elif request.args.get('followers'):
            users = User.query.filter_by(username=request.args.get('followers')).first().followers
            message = "{} user{} found".format(users.count(), "" if users.count() == 1 else "s")
        else:
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.index'))
    return render_template('users.html', users=users, message=message)



@bp.route('/delete_profile/', methods=['GET', 'DESTROY'])
@login_required
def delete_profile():
    # delete everything - danger zone!
    pass

@bp.route('/follow/<username>/')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('main.index'))
    if user == current_user:
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('main.user', username=username))

@bp.route('/unfollow/<username>/')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('main.index'))
    if user == current_user:
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('main.user', username=username))

@bp.route('/send_message/<recipient>/', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    # send a message to a given recipient
    pass

@bp.route('/messages/')
@login_required
def messages():
    # access my messages
    pass