from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from .models import User, Navigation, Education, Cv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re
import json

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        is_admin = request.form.get('is_admin', 0)
        if is_admin == 'on':
            is_admin = 1

        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if len(email) < 4 or not re.fullmatch(regex, email):
            flash('Email in invalid and must be longer than 3 characters',
                  category='error')
        elif len(full_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != confirm_password:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                full_name=full_name,
                email=email,
                is_admin=is_admin,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user)


@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    five_index = [1, 2, 3, 4, 5]
    users = User.query.all()
    navigation = Navigation.query.all()
    navigation_count = Navigation.query.count()
    education = Education.query.all()    
    education_count = Education.query.count()
    cvs = Cv.query.all()

    return render_template("admin.html", 
        users=users, 
        navigation=navigation, 
        education=education, 
        five_index=five_index, 
        user=current_user, 
        navigation_count=navigation_count, 
        education_count=education_count,
        cvs = cvs
    )


@auth.route('/profile_submit', methods=['POST'])
def profile_submit():
    if request.method == 'POST':
        user_id = request.form.get('profile_id')
        profile_name = request.form.get('profile_name')
        profile_email = request.form.get('profile_email')
        # password = request.form.get('password')
        # confirm_password = request.form.get('confirm_password')
        profile_number = request.form.get('profile_number')
        profile_skype = request.form.get('profile_skype')
        profile_git = request.form.get('profile_git')
        profile_location = request.form.get('profile_location')

        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        # if len(email) < 4 or not re.fullmatch(regex, email):
        #     flash('Email in invalid and must be longer than 3 characters', category='error')
        # elif len(full_name) < 2:
        #     flash('First name must be greater than 1 character.', category='error')
        # elif password != confirm_password:
        #     flash('Passwords don\'t match.', category='error')
        # elif len(password) < 7:
        #     flash('Password must be at least 7 characters.', category='error')
        # else:
        update_user = User.query.filter_by(id=user_id).first()
        if profile_name:
            update_user.full_name = profile_name
        if profile_email:
            update_user.email = profile_email
        if profile_number:
            update_user.contact_num = profile_number
        if profile_skype:
            update_user.skype = profile_skype
        if profile_location:
            update_user.location = profile_location
        if profile_git:
            update_user.github = profile_git

        db.session.commit()

        flash('Account updated!', category='success')

    return render_template("admin.html")


@auth.route('/navigation_sumbit', methods=['POST'])
def navigation_submit():
    if request.method == 'POST':
        navigation_link = request.form.get('navigation_link')

        new_nav_link = Navigation(
            title=navigation_link,
        )
        db.session.add(new_nav_link)
        db.session.commit()

        flash('Navigation link created!', category='success')

    return redirect(url_for('auth.admin', user=current_user))


@auth.route('/navigation_edit', methods=['POST'])
def navigation_edit():
    if request.method == 'POST':
        nav_id = request.form.get('navigation_edit_id')
        navigation_link = request.form.get('navigation_link')

        update_nav = Navigation.query.filter_by(id=nav_id).first()
        update_nav.title = navigation_link

        db.session.commit()

        flash('Navigation link edited!', category='success')

    return redirect(url_for('auth.admin'))


@auth.route('/delete-nav', methods=['POST'])
def delete_nav():
    nav = json.loads(request.data)
    navId = nav['navId']
    nav = Navigation.query.get(navId)

    db.session.delete(nav)
    db.session.commit()

    return jsonify({})

@auth.route('/education_submit', methods=['POST'])
def education_submit():
    if request.method == 'POST':
        education_title = request.form.get('education_title')
        education_desc = request.form.get('education_desc')   

        new_education = Education(
            # user_id = current_user.id
            title=education_title,
            desc=education_desc,
        )
        db.session.add(new_education)
        db.session.commit()

        flash('Education created!', category='success')

    return redirect(url_for('auth.admin', user=current_user))

@auth.route('/education_edit', methods=['POST'])
def education_edit():
    if request.method == 'POST':
        edu_id = request.form.get('education_edit_id')
        education_title = request.form.get('education_edit_title')
        education_desc = request.form.get('education_desc')        

        update_education = Education.query.filter_by(id=edu_id).first()
        if education_title:
            update_education.title = education_title
        if education_desc:
            update_education.desc = education_desc

        db.session.commit()

        flash('Education updated!', category='success')

    return redirect(url_for('auth.admin'))

@auth.route('/delete-education', methods=['POST'])
def delete_education():
    education = json.loads(request.data)
    educationId = education['educationId']
    education = Education.query.get(educationId)

    db.session.delete(education)
    db.session.commit()

    return jsonify({})


