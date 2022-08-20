from cmath import log
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, logout_user
from .models import Post, User
from . import db, app
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)



#For the home page
@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():

    if(request.method == 'POST'):
        post = request.form.get('post')

        if(len(post) < 1):

            flash('The post should not be empty', category='error')

        else:

            new_user_post = Post(post_data = post, user_id = current_user.id)
            db.session.add(new_user_post)
            db.session.commit()
            return redirect(url_for('views.post_view'))
        

    return render_template('home.html', user = current_user)

#For the home page
@views.route('/post_view')
@login_required
def post_view():


    posts = Post.query.all()
    users = User.query.all()
    return render_template('post_view.html', posts = posts, active_user = current_user, users = users)

#For logging out
@views.route('/logout')
@login_required
def logout():

    if(current_user.is_authenticated):
        logout_user()
    
    return redirect(url_for('auth.login'))

#For viewing the post
@views.route('/user_post/<int:id>')
@login_required
def view_post(id):

    post_to_view = Post.query.get(id)
    user = User.query.get(post_to_view.user_id)

    return render_template('view_user_post.html', user = user, post = post_to_view)

#For editting the post
@views.route('/edit_post/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_post(id):


    post_to_view = Post.query.get(id)
    user = User.query.get(post_to_view.user_id)

    if(request.method == 'POST'):

        post = request.form.get('post')
        post_to_view.post_data = post
        db.session.commit()
        return redirect(url_for('views.post_view'))

    return render_template('edit_post.html', user = user, post = post_to_view)

#For deleting the post
@views.route('/delete_post/<int:id>')
@login_required
def delete_post(id):

    post_to_view = Post.query.get(id)
    db.session.delete(post_to_view)
    db.session.commit()
    return redirect(url_for('views.post_view'))

#For viewing current user's post
@views.route('/my_posts')
@login_required
def my_posts():

    return render_template('my-post.html', user = current_user)


#For viewing the profile
@views.route('/my-profile', methods = ['GET', 'POST'])
@login_required
def profile():

    if(request.method == 'POST'):

        if 'file' not in request.files:
            flash('There is no file part', category='error')
            return redirect(request.url)

        file = request.files['file']

        if(file.filename == ''):
            flash('There is no image selected', category='error')
            return redirect(request.url)

      
        if(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_filename = filename
            db.session.commit()
            print(current_user.profile_filename)
            flash('Profile picture has been changed', category='success')
            return redirect(request.url)
           

    return render_template('profile.html', user = current_user)


@views.route('/change-username', methods = ['POST', 'GET'])
@login_required
def change_password():
    
    if(request.method == 'POST'):

        name = request.form.get('text')
        current_user.user_name = name
        db.session.commit()
        return redirect(url_for('views.profile'))

    return render_template('update-name.html', user = current_user)