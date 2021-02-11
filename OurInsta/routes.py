from flask import render_template, url_for, flash, redirect, request
from OurInsta import app, db
from OurInsta.models import Users
from flask_login import login_user, current_user, logout_user, login_required
import hashlib


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
        if password != confirm_password :
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

