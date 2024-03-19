from server import app
from model import Movie, db
from datetime import datetime
import sys
import os
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

app.app_context().push()

script_dir = os.path.dirname(os.path.abspath(__file__))
movies_json_path = os.path.join(script_dir, "data/movies.json")

def seed_movies():
    if os.path.exists(movies_json_path):
        with open(movies_json_path, 'r') as file:
            movies_data = json.load(file)
        
        for data in movies_data:
            title = data.get('title')
            overview = data.get('overview')
            release_date_str = data.get('release_date')
            poster_path = data.get('poster_path')

            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()

            movie = Movie(
                title=title,
                overview=overview,
                release_date=release_date,
                poster_path=poster_path
            )

            db.session.add(movie)

        db.session.commit()
        print("Movies seeded successfully.")
    else:
        print("movies.json file not found.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_movies()