from flask_bcrypt import Bcrypt, generate_password_hash
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def get_by_email(email):
    return User.query.filter_by(email=email).first()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)


    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)


    def __str__(self):
        return f"User Id: {self.id}"
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def json(self):
        return f"'id' : {self.id}, 'email' : {self.email}, 'password' : {self.password_hash}"
    



class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(255))
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    # ratings = a list of Rating objects

    def __init__(self, title, overview, release_date, poster_path):
        self.title = title
        self.overview = overview
        self.release_date = release_date
        self.poster_path = poster_path

    def json(self):
        return f"'id' : {self.id}, 'title' : {self.title}, 'overview' : {self.overview}, 'release_date' : {self.release_date}, 'poster_path' : {self.poster_path}"
    
    def __repr__(self):
        return f"<Movie id = {self.id} title = {self.title}>"
    

class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    review = db.Column(db.Text)

    movie = db.relationship("Movie", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __init__(self, score, movie_id, user_id, review):
        self.score = score
        self.movie_id = movie_id
        self.user_id = user_id
        self.review = review


    def json(self):
        return f"'id' : {self.id}, 'score' : {self.score}, 'movie_id' : {self.movie_id}, 'user_id' : {self.user_id}, 'review' : {self.review}"
    
    def __repr__(self):
        return f"<Rating id={self.rating_id} score={self.score}>"


def connect_to_db(flask_app, db_uri=None, echo=True):

    if db_uri is None:
        db_uri = "postgresql:///ratings"

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")



if __name__ == "__main__":
    from server import app
    connect_to_db(app, echo=False)