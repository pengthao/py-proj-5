from flask import Blueprint, render_template, redirect, request, url_for
from model import Movie, Rating, db
from movies.forms import AddRating
from flask_login import current_user


ratings_blueprint = Blueprint('ratings', __name__, template_folder='templates/ratings')

@ratings_blueprint.route('/my_ratings')
def my_ratings():

    user = int(current_user.id)
    print(f'user id print {user}')

    rating_data = []
    ratings = Rating.query.filter_by(user_id = user)
    for rating in ratings:
        movie = Movie.query.filter_by(id = rating.movie_id).first()
        rating.poster_path = movie.poster_path
        rating_data.append({"rating": rating, "movie": movie})
 
    return render_template('my_ratings.html', rating_data=rating_data)
