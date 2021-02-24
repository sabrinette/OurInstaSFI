from flask import render_template, url_for, flash, redirect, request, abort
from OurInsta import app, db
from OurInsta.models import Users , Post
from flask_login import login_user, current_user, logout_user, login_required
import hashlib
import os
from werkzeug.utils import secure_filename
import time


app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/')
def home():
    return render_template("base.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("you are already logged in !!", "danger")
        return redirect(url_for('home'))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.query(Users).filter(Users.email == email).first()
        if user is None :
            flash("this user doesn't exist", "danger")
            return redirect(url_for('register'))
        else:
            password_data = db.session.query(Users).filter(Users.email == email).filter(Users.secure_password == hashlib.md5(str(password).encode()).hexdigest()).first()
            if password_data is None:
                flash("incorrect password", "danger")
                return render_template("login.html")
            else:
                user.is_authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash("you are successfully logged in !", "success")
                return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route('/register',methods=["GET" , "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        flash("you are already logged in !!", "danger")
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        secure_password = hashlib.md5(str(password).encode()).hexdigest()
        user_email = db.session.query(Users).filter(Users.email == email).first()
        user_phone_number = db.session.query(Users).filter(Users.phone_number == phone_number).first()
        add = True
        if user_email is not None or user_phone_number is not None :
            add = False
            flash("user already exists , please login ", "danger")
            return redirect(url_for('login'))
        if password != confirm_password:
            add = False
            flash("verify password", "danger")
            return render_template("register.html")
        img_url = "default.png"
        if request.files:
            image = request.files["profile_picture"]
            if image.filename != '':
                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    filename = str(time.time())+"_"+filename
                    filename = filename.replace(".", "_", 1)
                    image.save(os.path.join('static/profile_images', filename))
                    img_url = filename
                else:
                    add = False
                    flash("only png , jpeg and jpg extensions are allowed", "danger")
        if add == True:
            usr = Users(name, phone_number, email, secure_password, img_url)
            usr.is_authenticated = True
            db.session.add(usr)
            db.session.commit()
            login_user(usr)
            flash("you are successfully logged in !", "success")
            return redirect(url_for('home'))
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")

@app.route('/editProfile', methods=["GET","POST"])
@login_required
def editProfile():
    if request.method == "POST":
        current_user.name = request.form.get("name")
        current_user.email = request.form.get("email")
        current_user.phone_number = request.form.get("phone_number")
        if hashlib.md5(str(request.form.get("current_password")).encode()).hexdigest() == current_user.secure_password:
            if request.form.get("new_password") == request.form.get("confirm_new_password"):
                current_user.secure_password = hashlib.md5(str(request.form.get("new_password")).encode()).hexdigest()
                db.session.commit()
                flash('Your account has been updated!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('rewrite the new password correctly!', 'danger')
                return render_template("editProfile.html")
        else:
            flash('old password incorrect!', 'danger')
            return render_template("editProfile.html")
    else:
        return render_template("editProfile.html")

@app.route("/logout")
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash("you are successfully logged out","success")
    return redirect(url_for('login'))

@app.route('/addPost', methods=["GET", "POST"])
@login_required
def addPost():
    if request.method == "POST":
        post_description = request.form.get("post_description")
        add = True
        img_url = ""
        if request.files:
            image = request.files["post_picture"]
            if image.filename != '':
                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    filename = str(time.time()) + "_" + filename
                    filename = filename.replace(".", "_", 1)
                    image.save(os.path.join('static/post_images', filename))
                    img_url = filename
                else:
                    add = False
                    flash("only png , jpeg and jpg extensions are allowed", "danger")
                    return render_template("addPost.html")
        if add == True :
            post = Post(post_description, img_url, current_user)
            db.session.add(post)
            db.session.commit()
        return redirect(url_for('profile',id=current_user.user_id))
    else:
        return render_template("addPost.html")

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = db.session.query(Post).filter(post_id == Post.post_id).first()
    comments = post.post_comments
    return render_template('post.html', post=post, comments=comments)

@app.route("/post/<int:post_id>/updatePost", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = db.session.query(Post).filter(post_id == Post.post_id).first()
    if post.author != current_user:
        abort(403)
    if request.method == "POST":
        post.post_description = request.form.get("post_description")
        image = request.files["post_picture"]
        filename = secure_filename(image.filename)
        image.save(os.path.join('static/post_images', filename))
        post.post_image = image.filename
        db.session.commit()
        flash('Your post has been successfully updated!', 'success')
        return redirect(url_for('profile',id=current_user.user_id))
    else :
        return render_template("updatePost.html", post=post)

@app.route("/post/<int:post_id>/deletePost", methods=['GET'])
@login_required
def delete_post(post_id):
    post = db.session.query(Post).filter(post_id == Post.post_id).first()
    if post.author != current_user:
        abort(403)
    os.remove('static/post_images/'+post.post_image)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been successfully deleted!', 'success')
    return redirect(url_for('home'))
