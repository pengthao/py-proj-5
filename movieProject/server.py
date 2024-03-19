from flask import Flask, render_template
from model import connect_to_db, login_manager, db
from flask_migrate import Migrate

custom_db_uri = "postgresql://postgres:password@localhost:5432/movieProject"

app = Flask(__name__)
app.config['SECRET_KEY'] ="Suersecretkey!"
Migrate(app, db)
connect_to_db(app, custom_db_uri)

login_manager.init_app(app)
login_manager.login_view = 'user.login'

@app.route('/')
def home():
    return render_template("home.html")

@app.errorhandler(404)
def error_404(e):
   return render_template("404.html")

from users.views import users_blueprint
from movies.views import movies_blueprint
from ratings.views import ratings_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(movies_blueprint, url_prefix='/movies')
app.register_blueprint(ratings_blueprint, url_prefix='/ratings')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")