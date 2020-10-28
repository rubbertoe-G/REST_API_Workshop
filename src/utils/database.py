from pymongo import MongoClient
from flask import jsonify
from utils.movie import MovieModel
from bson.objectid import ObjectId

mongo_client = MongoClient(
    host='localhost',
    port=27017,
    username='root',  # Username of the database
    password='Sup3rS1mpl3'  # Password of the database
)

db = mongo_client['movie_catalog']
collection = db['movies']


def get_movies(start=0, offset=50):
    """Get all movies. Paginate accordingly. Return only id, title and year of a movie. Return 50 values by default"""

    if offset >= 1000 or offset <=0:
        return jsonify({
            'ERROR': "Cant return more than 1000 records at a time. Please set offset query param less than 1000"
        }), 500

    if start < 0:
        return jsonify({
            'ERROR': 'Query string error. "string value cannot be less than 0"'
        }), 500

    cursor = collection.find(
        {}, {"_id": True, "title": True, "year": True}).skip(start).limit(offset)

    # Response list
    res_arr = list()

    # Iterate over database objects and populate cursom JSON response
    for item in cursor:
        movie_object = MovieModel(**item)
        custom_json = {
            'title': movie_object.title,
            'year': movie_object.year,
            'id': movie_object.id
        }
        res_arr.append(custom_json)

    return jsonify(res_arr)


def create_movie(body):
    """Insert a new movie into the database. use the movie model serialization."""
    # Insert movie to the database
    created_item = collection.insert_one(body)

    return jsonify({
        'message': 'Movie successfully created!',
        'id': str(created_item.inserted_id) ## Must be cast to str(). Raises TypeError: Object of type ObjectId is not JSON serializable 
    })


def get_movie_by_id(id):
    """Get a movie by id. Return all fields of a movie"""
    cursor = collection.find_one({'_id': ObjectId(id)})
    
    movie = None

    for m in cursor:
        movie = MovieModel(**m)
    
    return jsonify(movie.to_json())




def update_movie_by_id(id, movie_data):
    """Update the movie from the database by id"""
    pass


def remove_movie_by_id(id):
    """"Remove movie by id"""
    pass