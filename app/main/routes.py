from datetime import datetime
from flask import redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import User, Post


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    # get the title and first image of the most recent post
    return "HELLO"

@bp.route('/posts', methods=['GET'])
def posts():
    # get all posts
    pass

@bp.route('/tags/<tagname>', methods=['GET', 'POST'])
def tags():
    # get all the posts for the given tagname
    pass

@bp.route('/user/<username>')
@login_required
def user(username):
    # get the user's profile page
    pass


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