from flask import Blueprint, render_template, redirect, request, url_for
from model import Movie, Rating, db
from movies.forms import AddRating
from flask_login import current_user


movies_blueprint = Blueprint('movies', __name__, template_folder='templates/movies')

@movies_blueprint.route('/all_movies')
def all_movies():

    movies = Movie.query.all()

    return render_template('all_movies.html', movies=movies)


@movies_blueprint.route('/movie_details/<movie_id>', methods=["GET", "POST"])
def movie_details(movie_id):
    movie =  Movie.query.filter_by(id=movie_id).first()

    form = AddRating()

    if request.method == "POST":
        if form.validate_on_submit():
            user = current_user

            movieRating = Rating(
                score=form.score.data,
                movie_id=movie.id,
                user_id=user.id,
                review=form.review.data
            )

            db.session.add(movieRating)
            db.session.commit()

            return redirect(url_for('ratings.my_ratings'))

    return render_template('movie_details.html', movie=movie, form=form)

