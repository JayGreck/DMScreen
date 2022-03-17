import os
import secrets
from sqlalchemy.orm import load_only
from flaskdmscreen.models import Statblocks, Statblocks, User, Players
from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskdmscreen import app, db, bcrypt
from forms import RegistrationForm, LoginForm, EditProfileForm, UploadStatblock, AddToCombat, InitiativeForm, AddPlayerToCombat, PlayerForm, PlayerManager
from sqlalchemy import update
from flaskdmscreen.InitiativeVision import InitiativeVision
import random

@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
 
    upload_statblock_form = UploadStatblock()

    forms = []
    
    # Add new entry
    if upload_statblock_form.validate_on_submit():
        
        
        if upload_statblock_form.statblock.data:
           
            statblock_file = save_picture(upload_statblock_form.statblock.data, 'static/statblocks')

            add_statblock = Statblocks(user_id=current_user.id, statblock_file=statblock_file)
            
            db.session.add(add_statblock)
            db.session.commit()
            flash("Successful Statblock Upload!", 'success')
    
    
           
    image_names = os.listdir('flaskdmscreen/static/statblocks')

    test_dictionary = {}
    
   
    list1 = []
    for i in image_names:
        query = Statblocks.query.filter_by(statblock_file=i, user_id=current_user.id).options(load_only(Statblocks.statblock_file)) # Checking if current user has uploaded an image
        
        for j in query:
            list1.append(j.statblock_file) # Appending it to the list that will be passed to the home screen
    
    for list in list1:
        form = AddToCombat(prefix=list)
        test_dictionary[list] = form
    
    for key, form in test_dictionary.items():
        print(form.in_combat.data)
        if form.validate_on_submit():

            db.session.execute(update(Statblocks).where(Statblocks.statblock_file == key and Statblocks.user_id == current_user.id).values(in_combat=form.in_combat.data))
            db.session.commit()
            flash("Statblock Successfully Added to Combat", 'success')
    
        
    return render_template("home.html", upload_statblock_form=upload_statblock_form, image_file=test_dictionary, user_id=Statblocks.user_id, in_combat_form=forms) # statblocks=statblocks

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

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    
    image_file = url_for('static', filename= f'profile_pics/{current_user.image_file}')
    
    return render_template('account.html', title='Account', image_file=image_file)

def save_picture(form_picture, path):
    print("in save picture")
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, path, picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn


@app.route("/editprofile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    
    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/profile_pics')
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= f'profile_pics/{current_user.image_file}')
    return render_template('editprofile.html', title='Account Update', form=form, image_file=image_file)

@app.route("/initiativetracker", methods=['GET', 'POST'])
@login_required
def init_tracker():
    
    form = InitiativeForm()
    add_player_form = AddPlayerToCombat()
    
    # Generating choices from db
    add_player_form.player_name.choices = [(player_name.id, player_name.player_name)for player_name in Players.query.filter_by(user_id=current_user.id).options(load_only(Players.player_name))]

    statblocks = url_for('static', filename= f'statblocks/{Statblocks.statblock_file}')
    image_names = os.listdir('flaskdmscreen/static/statblocks')

    initiative_list = []
    statblock_name_list = []

    score_list = []
    image_file_list = []
    statblock_view_list = []
    statblock_side_list = []

    
    for s in image_names: 
        query = Statblocks.query.filter_by(statblock_file=s, user_id=current_user.id, in_combat=True).order_by(Statblocks.statblock_file, Statblocks.initiative_modifier, Statblocks.statblock_name) # Checking if current user has uploaded an image


        for i in query:

            if form.submit.data:
                
                if i.initiative_modifier == None:
                    initiative_vision = InitiativeVision(i.statblock_file)
                    initiative_detect_word = initiative_vision.detectWord()
                    modifier, score, name = initiative_detect_word
                    if (modifier == 1):
                        flash('One of the Statblocks Not Properly Read! Upload a Higher Resolution Image', 'warning')
                    else:
                        # Insert statblock name and modifier to db
                        db.session.execute(update(Statblocks).where(Statblocks.statblock_file == i.statblock_file and Statblocks.user_id == current_user.id).values(statblock_name=name, initiative_modifier=modifier, initiative_score=score))
                        db.session.commit()
                else:
                    # If the statblock has already been read in, stopping the computer vision algorithm from having to constantly run
                    score = random.randint(1,20) + i.initiative_modifier
                    name = i.statblock_name
                    score_list.append(score)
                    statblock_name_list.append(name)
                    print("score" + str(score))
                    image_file_list.append("statblocks/" + i.statblock_file)
                    db.session.execute(update(Statblocks).where(Statblocks.statblock_file == i.statblock_file and Statblocks.user_id == current_user.id).values(initiative_score=score))
                    db.session.commit()
            
                
                
                
                
    player_query = Players.query.filter_by(user_id=current_user.id, in_combat=True).order_by(Players.player_name, Players.initiative_score, Players.image_file) # Checking if current user has uploaded an image
    for player in player_query:
        if form.submit.data:
            player_score = player.initiative_score
            player_name = player.player_name
            image_file_list.append("player_images/" + player.image_file) 
            score_list.append(player_score)
            statblock_name_list.append(player_name)
    
    statblock_view_list = sorted(zip(score_list, image_file_list), reverse=True)
    statblock_side_list = sorted(zip(score_list, statblock_name_list), reverse=True)

    return render_template('initiativeTracker.html', title='Initiative Tracker', image_file=statblock_view_list, initiative_list=initiative_list, statblock_name_list=statblock_side_list, form=form, add_player_form=add_player_form)

@app.route("/AddPlayers", methods=['GET', 'POST'])
@login_required
def add_players():
    form = PlayerForm()

    if form.validate_on_submit():

        if form.data:
            player_name = form.player_name.data
            player_image = save_picture(form.picture.data, 'static/player_images')
            player = Players(user_id=current_user.id, player_name=player_name, image_file=player_image)
            db.session.add(player)
            db.session.commit()
    
    amt_players = []
    player_forms = {}

    player_query_test = Players.query.filter_by(user_id=current_user.id).order_by(Players.image_file, Players.id, Players.in_combat, Players.initiative_score, Players.player_name)

    for player in player_query_test:
        amt_players.append(player.player_name)
    
    for p in amt_players:
        player_form = PlayerManager(prefix=p)
        player_forms[p] = player_form

    
    for name, player_form in player_forms.items():
        print(name)
        
        if player_form.validate_on_submit():

            db.session.execute(update(Players).where(Players.player_name == name and Players.user_id == current_user.id).values(in_combat=player_form.in_combat.data, initiative_score=player_form.player_initiative_score.data))
            db.session.commit()
            flash("Statblock Successfully Added to Combat", 'success')

    return render_template('addPlayers.html', title='Add Players', form=form, inCombatForm=player_forms)

