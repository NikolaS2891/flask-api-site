from flask import render_template, request, redirect, url_for, flash
from flask_login import login_manager, login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt
from flask_app import app, db
from flask_app.models import *
from flask_app.forms import *

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    else:
        passwd1 = request.form.get('password1')
        passwd2 = request.form.get('password2')

        if passwd1 != passwd2 or passwd1 == None:
            flash('Password Error!', 'danger')
            return render_template('register.html')

        hashed_pass = sha256_crypt.encrypt(str(passwd1))

        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('username'),
            password=hashed_pass)

        if user_exsists(new_user.username, new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('register.html')
        else:
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash('Account created!', 'success')
            return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        result = User.query.filter_by(username=username).first()

        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            login_user(result)
            flash('Logged in!', 'success')
            return redirect(url_for('site'))

        else:
            flash('Incorrect Login!', 'danger')
            return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))

def user_exsists(username, email):
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    return False

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/site")
@login_required
def site():
    db.create_all()
    posts = SiteInput.query.all()
    app.logger.info('Processing default request')
    return render_template("index.html", posts=posts)

@app.route("/site/new", methods=['GET', 'POST'])
@login_required
def new_site():
    
    form = NewSiteInput()
    if form.validate_on_submit():
        post = SiteInput(cell_id=form.cell_id.data, azimuth=form.azimuth.data, band=form.band.data, username=current_user.username)
        db.session.add(post)
        db.session.commit()
        flash('Your site has been created!', 'success')
        return redirect(url_for('site'))
    return render_template('create_site.html', title='New Site',
                           form=form, legend='New Site')

@app.route("/site/<int:site_id>")
@login_required
def site_edit(site_id):
    post = SiteInput.query.get_or_404(site_id)
    form = NewSiteInput()
    
    return render_template('site.html', post= post)

@app.route("/site/<int:site_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(site_id):
    post = SiteInput.query.get_or_404(site_id)
    if post.username != current_user.username:
        abort(403)
    form = NewSiteInput()
    if form.validate_on_submit():
        post.cell_id = form.cell_id.data
        post.azimuth = form.azimuth.data
        post.band = form.band.data
        db.session.commit()
        flash('Your site has been updated!', 'success')
        return redirect(url_for('site', site_id=post.id))
    elif request.method == 'GET':
        form.cell_id.data = post.cell_id
        form.azimuth.data = post.azimuth
        form.band.data = post.band
    return render_template('create_site.html', title='Update Site',
                           form=form, legend='Update Site')

@app.route("/site/<int:site_id>/delete", methods=['POST'])
@login_required
def delete_post(site_id):
    post = SiteInput.query.get_or_404(site_id)
    if post.username != current_user.username:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your site has been deleted!', 'success')
    return redirect(url_for('index'))