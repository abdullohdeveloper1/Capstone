from flask import Flask, app, json, abort, request, jsonify
from database.models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resource={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, PATCH, DELETE, OPTIONS'
        )
        return response

    @app.route('/actors')
    @requires_auth('get:actor')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors],
            'total_actors': len(Actor.query.all())
        }), 200

    @app.route('/movies')
    @requires_auth('get:movie')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies],
            'total_movies': len(Movie.query.all())
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actors(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor_id,
                'total_actors': len(Actor.query.all())
            }), 200
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movies(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie_id,
                'total_movies': len(Movie.query.all())
            }), 200
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_actors(payload):
        body = request.get_json()
        try:
            name = body['name']
            age = body['age']
            gender = body['gender']
            actor = Actor(
                name=name,
                age=age,
                gender=gender
            )
            actor.insert()
            return jsonify({
                'success': True,
                'added': actor.id,
                'total_actors': len(Actor.query.all())
            }), 200
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_movies(payload):
        body = request.get_json()
        try:
            title = body['title']
            release_date = body['release_date']
            movie = Movie(
                title=title,
                release_date=release_date
            )
            movie.insert()
            return jsonify({
                'success': True,
                'added': movie.id,
                'total_movies': len(Movie.query.all())
            }), 200
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_actors(payload, actor_id):
        body = request.get_json()
        try:
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404)
            if 'name' in body:
                actor.name = body['name']
            if 'age' in body:
                actor.age = body['age']
            if 'gender' in body:
                actor.gender = body['gender']
            actor.update()
            return jsonify({
                'success': True,
                'total_actors': len(Actor.query.all())
            }), 200
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def patch_movies(payload, movie_id):
        body = request.get_json()
        try:
            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(404)
            if 'title' in body:
                movie.title = body['title']
            if 'release_date' in body:
                movie.release_date = body['release_date']
            movie.update()
            return jsonify({
                'success': True,
                'total_movies': len(Movie.query.all())
            })
        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request.'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found.'
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed.'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable.'
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error.'
        }), 500

    @app.errorhandler(AuthError)
    def auth(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


