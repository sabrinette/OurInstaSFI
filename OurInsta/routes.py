from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from OurInsta import app, db
from OurInsta.models import Users, Post, Reaction, Comment , followers
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
def hello():
    return render_template("base.html")

@app.route('/addReaction', methods=["POST"])
@login_required
def addReaction():
    post_id = request.form.get("id_post")
    user_id = current_user.user_id
    reaction_type = request.form.get("reaction_type")
    if reaction_type == "1":
        reaction_type = 1
    elif reaction_type == "0":
        reaction_type = 0
    reaction = db.session.query(Reaction).filter(Reaction.post_id == post_id).filter(Reaction.user_id == user_id).first()
    if reaction is None:
        deleted = 0
        reaction = Reaction(user_id, post_id, reaction_type)
    else:
        if reaction_type == reaction.reaction_type:
            deleted = 1
        else:
            deleted = 0
        reaction.reaction_type = reaction_type
    if deleted == 1:
        db.session.delete(reaction)
    else:
        db.session.add(reaction)
    db.session.commit()
    nb_likes = db.session.query(Reaction).filter(Reaction.reaction_type == 1).filter(Reaction.post_id == post_id).count()
    nb_unlikes = db.session.query(Reaction).filter(Reaction.reaction_type == 0).filter(Reaction.post_id == post_id).count()
    data = {'deleted': deleted, 'nb_likes': nb_likes, 'nb_unlikes': nb_unlikes}
    return jsonify(data)

@app.route('/dashbord', methods=["GET","POST"])
@login_required
def dashbord():
    posts = db.session.query(Post).all()
    nb_posts = db.session.query(Post).count()
    Total_post_size = 0
    for post in posts:
        stats = os.stat('OurInsta/static/post_images/' + post.post_image)
        Total_post_size = Total_post_size + stats.st_size
    nb_user_posts = current_user.posts.count()
    usr_post_size = 0
    for post in current_user.posts:
        stats = os.stat('OurInsta/static/post_images/' + post.post_image)
        usr_post_size = usr_post_size + stats.st_size
    return render_template("dashbord.html", Total_post_size=Total_post_size, nb_posts=nb_posts, usr_post_size=usr_post_size,nb_user_posts=nb_user_posts)

@app.route('/home')
@login_required
def home():
    nb_followers = db.session.query(followers).filter(current_user.user_id == followers.c.followed_id).count()
    page = request.args.get('page', 1, type=int)
    followed_posts = current_user.followed_posts().paginate(page=page, per_page=3)
    return render_template('home.html', posts= followed_posts , nb_followers=nb_followers)

@app.route('/user/<int:user_id>')
@login_required
def profile(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    nb_followers = db.session.query(followers).filter(user.user_id == followers.c.followed_id).count()
    posts = user.posts
    return render_template("profile.html", posts=posts, user=user, nb_followers=nb_followers)

@app.route('/editProfile', methods=["GET","POST"])
@login_required
def editProfile():
    if request.method == "POST":
        img_url = current_user.profile_image
        if request.files:
            image = request.files["profile_picture"]
            if image.filename != '':
                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    filename = str(time.time()) + "_" + filename
                    filename = filename.replace(".", "_", 1)
                    image.save(os.path.join('OurInsta/static/profile_images', filename))
                    img_url = filename
                else:
                    flash("only png , jpeg and jpg extensions are allowed", "danger")
        current_user.profile_image = img_url
        current_user.name = request.form.get("name")
        current_user.email = request.form.get("email")
        current_user.phone_number = request.form.get("phone_number")
        if hashlib.md5(str(request.form.get("current_password")).encode()).hexdigest() == current_user.secure_password:
            if request.form.get("new_password") == request.form.get("confirm_new_password"):
                current_user.secure_password = hashlib.md5(str(request.form.get("new_password")).encode()).hexdigest()
                db.session.commit()
                flash('Your account has been updated!', 'success')
                return redirect(url_for('profile', user_id=current_user.user_id))
            else:
                flash('rewrite the new password correctly!', 'danger')
                return render_template("editProfile.html")
        else:
            flash('old password incorrect!', 'danger')
            return render_template("editProfile.html")
    else:
        return render_template("editProfile.html")

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
                    image.save(os.path.join('OurInsta/static/profile_images', filename))
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
                    image.save(os.path.join('OurInsta/static/post_images', filename))
                    img_url = filename
                else:
                    add = False
                    flash("only png , jpeg and jpg extensions are allowed", "danger")
                    return render_template("addPost.html")
        if add == True :
            post = Post(post_description, img_url, current_user)
            db.session.add(post)
            db.session.commit()
        return redirect(url_for('profile',user_id=current_user.user_id))
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
        image.save(os.path.join('OurInsta/static/post_images', filename))
        post.post_image = image.filename
        db.session.commit()
        flash('Your post has been successfully updated!', 'success')
        return redirect(url_for('profile',user_id=current_user.user_id))
    else :
        return render_template("updatePost.html", post=post)

@app.route("/post/<int:post_id>/deletePost", methods=['GET'])
@login_required
def delete_post(post_id):
    post = db.session.query(Post).filter(post_id == Post.post_id).first()
    if post.author != current_user:
        abort(403)
    os.remove('OurInsta/static/post_images/'+post.post_image)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been successfully deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/addComment", methods=['POST'])
@login_required
def addComment():
    data = {'user_name': current_user.name, 'user_profile_image': current_user.profile_image, 'comment': request.form.get("comment_content")}
    user_id = current_user.user_id
    post_id = request.form.get("id_post")
    content = request.form.get("comment_content")
    comment = Comment(user_id,post_id,content)
    db.session.add(comment)
    db.session.commit()
    return jsonify(data)

@app.route("/post/<int:post_id>/deleteComment/<int:comment_id>", methods=['GET'])
@login_required
def delete_comment(comment_id,post_id):
    comment = db.session.query(Comment).filter(comment_id == Comment.comment_id).first()
    if comment.author_comment != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been successfully deleted!', 'success')
    return redirect("/post/"+str(post_id))

@app.route('/results', methods=['GET', 'POST'])
@login_required
def search_results():
    if request.method == "POST":
        search_key = request.form.get("search_key")
        results = db.session.query(Post).all()
        if search_key != '':
            search = "%{}%".format(search_key)
            results = db.session.query(Post).filter(Post.post_description.like(search)).all()
        return render_template('results.html', posts=results)
    else:
        return render_template("home.html")

@app.route('/follow/user/<int:user_id>')
@login_required
def follow(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        flash('User is not found.', 'danger')
        return redirect(url_for('home'))
    if user == current_user:
        flash('You can\'t follow yourself!', "danger")
        return redirect(url_for(profile, user_id=user_id))
    u = current_user.follow(user)
    if u is None:
        flash('Cannot follow ' + user.name + '.', "danger")
        return redirect(url_for('profile', user_id=current_user.user_id))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + user.name + '!', "success")
    return redirect(url_for('profile', user_id=user_id))

@app.route('/unfollow/user/<int:user_id>')
@login_required
def unfollow(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        flash('User is not found.' ,'danger')
        return redirect(url_for('home'))
    if user == current_user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('profile', user_id=user_id))
    u = current_user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ','danger')
        return redirect(url_for('profile', user_id=user_id))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ', 'success')
    return redirect(url_for('profile', user_id=user_id))

@app.route('/userSearchResults', methods=['GET', 'POST'])
@login_required
def userSearchResults():
    if request.method == "POST":
        search_user_name = request.form.get("search_user_name")
        results = db.session.query(Users).all()
        if search_user_name != '':
            search = "%{}%".format(search_user_name)
            results = db.session.query(Users).filter(Users.name.like(search)).all()
        return render_template('userSearchResults.html', users=results)
    else:
        return render_template("home.html")
