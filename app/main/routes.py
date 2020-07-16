from datetime import datetime
from flask import render_template, redirect, url_for, request, g, jsonify, current_app, flash
from flask_login import current_user, login_required
from flask_mail import Message
from markupsafe import escape
from sqlalchemy.sql import text
from app import db, mail
from app.main import bp
from app.auth import routes
from app.filters import check_confirmed
from app.main.forms import EditProfileForm, PostForm, CommentForm, SelectHeroPartial, ImageForm
from app.models import *
from werkzeug.http import HTTP_STATUS_CODES
from cloudinary.uploader import upload as _cloudinary_upload
import os
import pdb

# @bp.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.lastLoggedIn = datetime.utcnow()
#         db.session.commit()

@bp.route('/', methods=['GET'])
@bp.route('/index/', methods=['GET']) #always put a trailing /
def index():
    # get the title and first image of the most recent post
    latest_post = Post.query.filter(Post.isLive==True).order_by(Post.datePosted.desc()).first()
    return render_template('index.html', title='index page', post=latest_post)

@bp.route('/path/<path:subpath>/', methods=['GET'])
def subpath_test(subpath):
    return 'Subpath %s' % subpath

@bp.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')

@bp.route('/privacy-policy/', methods=['GET'])
def privacy():
    return render_template('privacy.html')

## POSTS #####################################################
@bp.route('/posts/', methods=['GET', 'POST'])
def posts():
    """
        render all the posts, filtered by:
        - tag: tag
        - user_id: written by provided user_id - for seeing drafts
        - liked: liked by the provided user

        if no args provided, just return all the live posts
    """
    if request.args:
        if request.args.get('tag'):
            tag = find_tag(request.args.get('tag'))
            posts = get_posts_for_tag(tag.id)
        elif request.args.get('user_id'):
            if request.args.get('isLive') and current_user.is_authenticated and str(current_user.id) == request.args.get('user_id'):
                posts = get_posts_by_user(user_id=request.args.get('user_id'), isLive=request.args.get('isLive'))
            else:
                user = User.query.filter_by(id=request.args.get('user_id')).first_or_404()
                return redirect(url_for('main.user', username=user.username))
        elif request.args.get('liked'):
            user = User.query.filter_by(username=request.args.get('liked')).first()
            posts = user.liked_posts.filter(Post.isLive==True).order_by(Post.datePosted.desc()).all()
        else:
            posts = []
            message = "not found"
    else:
        posts = Post.query.filter(Post.isLive==True).order_by(Post.datePosted.desc()).all()
        message = None
    number = len(posts) if type(posts) == list else posts.count()
    message = "{} post{} found".format(number, "" if number == 1 else "s")
    return render_template('posts.html', posts=posts, message=message, title="Posts")

@bp.route('/posts/new/', methods=['GET', 'POST'])
@login_required
def post_new():
    if current_user.isWriter:
        form = PostForm()
        form.selectHeroList.choices = Image.get_all_images_choices()
        if form.validate_on_submit():
            post = save_post(title=form.title.data, body=form.body.data, author=current_user, datePosted=datetime.utcnow())
            tags = escape(break_up_tags(post, form.tags.data))
            hero = post.set_post_hero_image(form.selectHeroList.data)
            #upload_image(form.images.data, post) ???
            return redirect(url_for('main.post', post_id=post.id))
        print(form.errors)
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
    form.selectHeroList.choices = Image.get_all_images_choices() #post.get_hero_image_choices() # fix this post.get_hero_image_choices()
    form.removeImages.choices = post.get_image_choices() #[(image.asset_id, image.id) for image in post.images] if post.images else []
    if post.author == current_user:
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            tags = escape(break_up_tags(post, form.tags.data))
            hero = post.set_post_hero_image(form.selectHeroList.data)
            remove_images = post.remove_images_from_post(form.removeImages.data)
            db.session.commit()
            upload_image(form.images.data, post)
            return redirect(url_for('main.post', post_id=post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.selectHeroList.data = post.get_post_hero_image_for_forms()
            form.body.data = post.body
            form.tags.data = ','.join([tag.name for tag in post.posttags.all()])
        return render_template('_post.html', form=form, post=post)
    else:
        return redirect(url_for('main.index'))

@bp.route('/posts/<post_id>/edit/delete/', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post:
        # delete any likes associated with this post !
        db.session.delete(post)
        db.session.commit()
        response = jsonify({'current_user': current_user.id, 'next': url_for('main.user', username=current_user.username)})
        response.status_code = 202
        redirect(url_for('main.user', username=current_user.username))
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

@bp.route('/golive/<post_id>')
@login_required
def golive(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post is None or (post.author != current_user):
        return redirect(url_for('main.index'))
    post.postToggleLive()
    db.session.commit()
    return redirect(url_for('main.post', post_id=post.id))

@bp.route('/makedraft/<post_id>')
@login_required
def makedraft(post_id):
    post = post = Post.query.filter_by(id=post_id).first_or_404()
    if post is None or (post.author != current_user):
        return redirect(url_for('main.index'))
    post.postToggleLive()
    db.session.commit()
    return redirect(url_for('main.post', post_id=post.id))

## COMMENTS ##################################################

@bp.route('/comment/new/', methods=['GET', 'POST'])
@login_required
def comment():
    form = CommentForm()
    pass
    

## IMAGES ###################################################

@bp.route('/images/', methods=['GET'])
@login_required
def images():
    images = Image.query.order_by(Image.id.desc()).all()
    return render_template('images.html', images=images, title="Images")

@bp.route('/images/<asset_id>')
@login_required
def image(asset_id):
    image = Image.query.filter_by(asset_id=asset_id).first()
    posts = image.posts.all()
    return render_template('image.html', image=image, posts=posts)


@bp.route('/images/upload/', methods=['GET', 'POST'])
@login_required
def images_upload():
    form = ImageForm()
    if form.validate_on_submit():
        images = upload_image(form.images.data)
        return redirect(url_for('main.images'))
#         if request.files['file'].content_type in ['image/gif', 'image/jpeg', 'image/png']: 
#             ## 'video/mp4'
#             ## Also need to check for file size!!!
#             file = request.files['file']
#             filename = "{}{}".format(user.id, user.username)
    return render_template('_image.html', form=form)

@bp.route('/images/<asset_id>/delete/', methods=['POST'])
@login_required
def images_delete(asset_id):
    image = Image.query.filter_by(asset_id=asset_id).first()
    image.delete_image()
    response = jsonify({'next': url_for('main.images')})
    response.status_code = 202
    #redirect(url_for('main.images'))
    return response
    
## USERS #####################################################

@bp.route('/user/<username>/', methods=['GET'])
@login_required
@check_confirmed
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = get_posts_by_user(user_id=user.id)
    return render_template('user.html', user=user, posts=posts)


@bp.route('/user/<username>/feed/')
@login_required
def user_feed(username):
    """
        The user's 'feed', get all the live posts of this user
    """
    user = User.query.filter_by(username=username).first_or_404()
    if current_user != user:
        return redirect(url_for('main.posts'))
    posts = Post.posts_by_user_follow(user)       
    number = len(posts) if type(posts) == list else posts.count()
    #message = "{} post{} found".format(number, "" if number == 1 else "s")
    return render_template('posts.html', posts=posts, message=None)


@bp.route('/user/<username>/edit/', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = escape(form.username.data)
        current_user.profile = escape(form.profile.data)
        current_user.profile_picture = current_user.set_profile_photo(form.profile_picture.data)
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
        elif request.args.get('liked_post'):
            post = Post.query.filter_by(id=request.args.get('liked_post')).first()
            users = post.likers
            message = "{} user{} found".format(users.count(), "" if users.count() == 1 else "s") # grrr
        else:
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.index'))
    return render_template('users.html', users=users, message=message, title="Users")



@bp.route('/delete_profile/<user>', methods=['DELETE'])
@login_required
def delete_profile(user):
    # delete everything - danger zone!
    # all of the below needs to actually be tested first
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