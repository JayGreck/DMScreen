from flaskdmscreen.models import User
from flask import redirect, url_for, render_template, flash, request
import flask_wtf
from flask_login import login_user, current_user, logout_user, login_required
from flaskdmscreen import app, db, bcrypt
from forms import RegistrationForm, LoginForm

@app.route("/")
@login_required
def home():
    
    # if request.method == "POST":
    #     statblock = request.form['name']
    #     new_statblock = Statblock(statblock=statblock)

    #     # Push to database
    #     try:
    #         db.session.add(new_statblock)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return "There was an arror adding your statblock...."
    # else:
    #     statblocks = Statblock.query()
    # statblock = request.files['statblock']

    # if not statblock:
    #     return "No statblock uploaded", 400
    
    # filename = secure_filename(statblock.filename)
    # mimetype = statblock.mimetype
    # img = Statblock(statblock=statblock.read(), mimetype=mimetype)
    # db.session.add(img)
    # db.session.commit()


    
    
    return render_template("home.html") # statblocks=statblocks

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("In validation")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", 'success')
        return redirect(url_for('login'))
    else:
        print("Incorrect Data")
    return render_template('register.html', title='Register', form=form)
   
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # Logic for logging in the user
        user = User.query.filter_by(email=form.email.data).first() # Checks if there are any emails in the database with that same data
        if user and bcrypt.check_password_hash(user.password, form.password.data): # Checks email exists in database, and password is correct to the one that is stored in the database
            login_user(user, remember=form.remember.data) # Logs in user, and if remember me is checked, their login will be saved to a cookie
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) # Redirects to home, or if another page was attempted to be accessed before login, redirect to attempted page once logged in
        else:
            flash('Login Unsuccessful. Please check login credentials', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
   

