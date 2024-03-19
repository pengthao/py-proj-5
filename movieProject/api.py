from flask import request
from flask_restful import Resource, Api
from movieProject import app, db
from movieProject.model import User, Movie, Rating
from datetime import datetime

api = Api(app)


############### Rest ###############
######### user api #################
    

class userDetails(Resource):
    def get(self, email):
        user = User.query.filter_by(email=email).first()

        if user:
            return user.json()
        else:
            return {'name': None},  404
        
class addUser(Resource):
    def post(self):

        data = request.get_json()

        email = data.get('email')
        password_h = data.get('password_h')
    
        user = User(
            email,
            password_h
        )

        db.session.add(user)
        db.session.commit()

        return user.json()

class deleteUser(Resource):

    def delete(self,email):
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()

        return {'note': 'delete success'}
    
class allUsers(Resource):

    def get(self):
        users = User.query.all()
        return [user.json() for user in users]
    

api.add_resource(userDetails,'/userinfo/<string:name>')
api.add_resource(allUsers,'/allusers')
api.add_resource(addUser,'/adduser')
api.add_resource(deleteUser,'/deleteuser/<string:name>')



######### Movie api ###############


class movieDetails(Resource):
    def get(self, title):
        movie = Movie.query.filter_by(title=title).first()

        if movie:
            return movie.json()
        else:
            return {'name': None},  404
        
class addMovie(Resource):
    def post(self):

        data = request.get_json()

        title = data.get('title')
        overview = data.get('overview')
        release_date_str = data.get('release_date')
        poster_path = data.get('poster_path')

        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
    
        movie = Movie(title,
                     overview,
                     release_date,
                     poster_path
                    )

        db.session.add(movie)
        db.session.commit()

        return movie.json()

class deleteMovie(Resource):

    def delete(self,title):
        movie = Movie.query.filter_by(title=title).first()
        db.session.delete(movie)
        db.session.commit()

        return {'note': 'delete success'}
    
class allMovies(Resource):

    def get(self):
        movies = Movie.query.all()
        return [movie.json() for movie in movies]
    

api.add_resource(movieDetails,'/moviedetails/<string:name>')
api.add_resource(allMovies,'/allmovies')
api.add_resource(addMovie,'/addmovie')
api.add_resource(deleteMovie,'/deletemovie/<string:name>')


######### Ratings api ###############



class ratingDetails(Resource):
    def get(self, id):
        rating = Rating.query.filter_by(id=id).first()

        if rating:
            return rating.json()
        else:
            return {'name': None},  404
        
class addRating(Resource):
    def post(self):

        data = request.get_json()

        score = data.get('score')
        movie = Movie.query.filter_by(title = data.get('title')).first()
        movie_id = movie.id
        user = User.query.filter_by(email = data.get('email')).first()
        user_id = user.id

    
        rating = Rating(score,
                     movie_id,
                     user_id
                    )

        db.session.add(rating)
        db.session.commit()

        return rating.json()

class deleteRating(Resource):

    def delete(self,id):
        rating = Rating.query.filter_by(id=id).first()
        db.session.delete(rating)
        db.session.commit()

        return {'note': 'delete success'}
    
class allRatings(Resource):

    def get(self):
        ratings = Rating.query.all()
        return [rating.json() for rating in ratings]
    

api.add_resource(ratingDetails,'/ratingdetails/<int:id>')
api.add_resource(allRatings,'/allratings')
api.add_resource(addRating,'/addrating')
api.add_resource(deleteRating,'/deleterating/<int:id>')