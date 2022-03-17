from sqlalchemy.orm import defaultload, relationship
from flaskdmscreen import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="defaultProfileImage.png")
    password = db.Column(db.String(60), nullable=False)
    statblock = db.relationship('Statblocks', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Statblocks(db.Model):
    __tablename__ = 'statblocks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    statblock_file = db.Column(db.String(20), nullable=True)
    in_combat = db.Column(db.Boolean, nullable=False, default=False)
    
    # ------------- TO BE ADDED -------------------#
    initiative_modifier = db.Column(db.Integer)
    initiative_score = db.Column(db.Integer)
    statblock_name = db.Column(db.String(20))
    # ------------- TO BE ADDED -------------------#

class Players(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_name = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="defaultProfileImage.png")
    in_combat = db.Column(db.Boolean, nullable=False, default=False)
    initiative_score = db.Column(db.Integer)
    
