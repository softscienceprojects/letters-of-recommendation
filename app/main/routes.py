from datetime import datetime
from flask import render_template, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from markupsafe import escape
from sqlalchemy.sql import text
from app import db
from app.main import bp
from app.auth import routes
from app.main.forms import EditProfileForm, PostForm, CommentForm
from app.models import *
from werkzeug.http import HTTP_STATUS_CODES


@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET'])
def index():
    # get the title and first image of the most recent post
    latest_post = Post.query.order_by(Post.datePosted.desc()).first()
    return render_template('index.html', title='index page', post=latest_post)

@bp.route('/path/<path:subpath>/', methods=['GET'])
def subpath_test(subpath):
    return 'Subpath %s' % subpath


## POSTS #####################################################
@bp.route('/posts/', methods=['GET', 'POST'])
def posts():
    """
        render all the posts, filtered by:
        - tag
        - written by a user (with given user_id)
        - liked by the current_user (to finish)
    """
    if request.args:
        if request.args.get('tag'):
            posts = Post.query.filter_by(tag=request.args.get('tag'))
        elif request.args.get('user_id'):
            posts = Post.query.filter_by(user_id=request.args.get('user_id'))
        # elif request.args.get('liked'):
        #     posts = Post.query.filter_by()
        else:
            posts = None
            message = "not found"
    else:
        posts = Post.query.all()
        message = None
    if posts:
        number = len(posts) if type(posts) == list else posts.count()
        message = "{} post{} found".format(number, "" if number == 1 else "s")
    return render_template('posts.html', posts=posts, message=message)

@bp.route('/posts/new/', methods=['GET', 'POST'])
@login_required
def post_new():
    if current_user.isWriter:
        form = PostForm()
        if form.validate_on_submit():
            post = save_post(title=form.title.data, body=form.body.data, author=current_user, datePosted=datetime.utcnow())
            print(post)
            tags = escape(break_up_tags(post, form.tags.data))
            print(tags)
            return redirect(url_for('main.post', post_id=post.id))
        return render_template('_post.html', form=form, post=None)
    else:
        return redirect(url_for('main.index'))


@bp.route('/posts/<post_id>/', methods=['GET'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    # if request.args.get('following'):
    # users = User.query.filter_by(username=request.args.get('following')).first().followed
    # message = "{} user{} found".format(users.count(), "" if users.count() == 1 else "s")
    return render_template('post.html', post=post)

@bp.route('/posts/<post_id>/edit/', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(post)
    if post.author == current_user:
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            tags = escape(break_up_tags(post, form.tags.data))
            print(tags)
            db.session.commit()
            return redirect(url_for('main.post', post_id=post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body
            form.tags.data = ':)'
            print(get_tags_for_post(post.id))
        return render_template('_post.html', form=form, post=post)
    else:
        return redirect(url_for('main.index'))

@bp.route('/posts/<post_id>/delete/', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post:
        # Post.query.filter_by(id=post_id).delete()
        db.session.delete(post)
        db.session.commit()
        response = jsonify({'current_user': current_user.id, 'next': url_for('main.user', username=current_user.username)})
        response.status_code = 202
        #response.headers['Location']
        #redirect(url_for('main.user', username=current_user.username))
        return response


@bp.route('/like/<post_id>/')
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post is None:
        return redirect(url_for('main.index'))
    current_user.like_post(post)
    db.session.commit()
    return redirect(url_for('main.post', post_id=post.id))

@bp.route('/unlike/<post_id>/')
@login_required
def unlike(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post is None:
        return redirect(url_for('main.index'))
    current_user.unlike_post(post)
    db.session.commit()
    return redirect(url_for('main.post', post_id=post.id))

## COMMENTS ##################################################

@bp.route('/comment/new/', methods=['GET', 'POST'])
@login_required
def comment():
    form = CommentForm()
    pass


## USERS #####################################################

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
        current_user.username = escape(form.username.data)
        current_user.profile = escape(form.profile.data)
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



@bp.route('/delete_profile/<user>', methods=['DELETE'])
@login_required
def delete_profile(user):
    # delete everything - danger zone!
    user = Post.query.filter_by(id=user.id).first_or_404()
    if user:
        # Post.query.filter_by(id=post_id).delete()
        db.session.delete(user)
        logout_user()
        db.session.commit()
        return redirect(url_for('main.index'))


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