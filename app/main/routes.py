from datetime import datetime
from flask import render_template, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from app import db
from app.main import bp
from app.models import User, Post


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    # get the title and first image of the most recent post
    return render_template('index.html', title='index page')

@bp.route('/path/<path:subpath>', methods=['GET'])
def subpath_test(subpath):
    # get the title and first image of the most recent post
    return 'Subpath %s' % subpath


@bp.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@bp.route('/posts/<post_id>', methods=['GET'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post)

@bp.route('/tags/<tagname>', methods=['GET', 'POST'])
def tags():
    # get all the posts for the given tagname
    pass

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # user can edit profile - bio, email, password
    pass

@bp.route('/delete_profile', methods=['GET', 'DESTROY'])
@login_required
def delete_profile():
    # delete everytihng - danger zone!
    pass

@bp.route('/follow/<username>')
@login_required
def follow(username):
    #follow provided user
    pass

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    # unfollow... should this be id instead?
    pass

@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    # send a message to a given recipient
    pass

@bp.route('/messages')
@login_required
def messages():
    # access my messages
    pass