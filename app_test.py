import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db, Actor, Movie

Assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkliUGlMcTJETGJyNDBrRUZ5enBZUiJ9.eyJpc3MiOiJodHRwczovL2FiZHVsbG9oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTFiOTYxNzIwMWMyZTAwNjk4NWRhNGYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyOTM4ODA2OSwiZXhwIjoxNjI5Mzk1MjY5LCJhenAiOiJqOHRIWGdVcmgyOXZPekloUEwwMmgzbktiNzhUaDhwSSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.REVVxZXzOEjM-8V791aiJhPCN3YqA4rSZA6Tm4rlzbHh47Zr7ojSdAnOU2atIOg0VX0kuewtIQEVObfBIDFwMEoZ9_yXJiSbyGDzi3V5U3Ys0GEGL5-YvgOJIlycUVXT4F2WqM75QDM6JsBiyMMzrA76faRieiWbejMbnLDK5_e5jkaazHJ76sQ6xcn9eFwsNnkF96gZmX7gy7qsvgcqm-GQQxbCiaQ6SSc7_omHD8_vDjih0o37v39NoE4DRhprqRSqVTQalGnzoPzjk7EqWBeIQKZu6tDNYcij5NcnIxn_BJAFwSY7DUOi4DgGRYl8Ps_n2UlUmF0RSit2-ra5iQ'
Director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkliUGlMcTJETGJyNDBrRUZ5enBZUiJ9.eyJpc3MiOiJodHRwczovL2FiZHVsbG9oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTFiOTY0YTViM2FiMzAwNjhjMmY3OWIiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyOTM4Njk5NywiZXhwIjoxNjI5Mzk0MTk3LCJhenAiOiJqOHRIWGdVcmgyOXZPekloUEwwMmgzbktiNzhUaDhwSSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.llb8H_z-iGDCx_GZx1d-SHx3gJrLvJyrYU5Fc3G_xpjtDIws1En2a9evQC0L_wpnpdCmvXwfH2-JuxUUqwzcLJMB-NY2Uo_Ne5w573UDQdPxUvmDmkexGOmEDiZGBh4asrUrR3_YcdbYRNiFP82e25belFMX32YXJqs0QqDtyVRVy_5kvpeZIxguROwwcM7_QaPSqi4oxYZU84rTNDYfbA6XDCHTUgY25czmnb5HR3DoLqLgH_1igfBnzl9xrt40xAEQjhwkR2H9Jm3OW0RUv5X6ITOwzmWkjiWOy9zF_I28CJ9PNiXmE_HSt3qUn1_tt8Hxv6uvJtfBrDFtZpzNoA'
Producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkliUGlMcTJETGJyNDBrRUZ5enBZUiJ9.eyJpc3MiOiJodHRwczovL2FiZHVsbG9oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTFhMTk2MzQ4NWY1YTAwNjg5OGFmOWIiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyOTM4Njg1NiwiZXhwIjoxNjI5Mzk0MDU2LCJhenAiOiJqOHRIWGdVcmgyOXZPekloUEwwMmgzbktiNzhUaDhwSSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.A8j-NiAnpcQN-pb5hGDdfqTr71AHMyIoXExAvIrEqzVifwLKQBvl--SjqIzUyc9fSYlkvxrMBqyHDGs-W7E55VRM8_pLD1ci35iqOcyX2s1lBo3weMuIYZn6TXmH6WhPeaLEGFjI_Hwk8FTDVrxBfrUp7f-1D5el5NT3MqkQhmp8Hu6LdmFS2nUdch8ccKarEXMP0eCgN-a7MSr-Y6es7-bB5ymtSxdkSFz2xOgr856rQ2jaAHU2uespq70YNphmktao7j0g_WG4QNvhvRxhZiakGt97FGzjcfpNOer0o8j_VwZnrzcWZpeKFDsrE-P5rBtEYrcdS9wwpUxaj16gyQ'


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'capstone_test'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            'postgres', '12', 'localhost:5432', self.database_name
        )
        setup_db(self.app, self.database_path)
        self.new_actor = {
            'name': 'Person',
            'age': 45,
            'gender': 'F'
        }
        self.new_movie = {
            'title': 'Movie',
            'release_date': 'January 5'
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            "Authorization": f"Bearer {Assistant}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_get_actors_404(self):
        res = self.client().get('/actor', headers={
            "Authorization": f"Bearer {Assistant}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Resource not found.')

    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            "Authorization": f"Bearer {Assistant}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_get_movies_404(self):
        res = self.client().get('/movie', headers={
            "Authorization": f"Bearer {Assistant}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Resource not found.')

    def test_post_actors(self):
        res = self.client().post('/actors', headers={
            "Authorization": f"Bearer {Director}"}, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_actors_405(self):
        res = self.client().post('/actors/55', headers={
            "Authorization": f"Bearer {Director}"}, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed.")

    def test_post_actors_rbac_assistant(self):
        res = self.client().post('/actors', headers={
            "Authorization": f"Bearer {Assistant}"}, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_post_movies(self):
        res = self.client().post('/movies', headers={
            "Authorization": f"Bearer {Producer}"}, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_movies_405(self):
        res = self.client().post('/movies/55', headers={
            "Authorization": f"Bearer {Producer}"}, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed.")

    def test_post_movies_rbac_assistant(self):
        res = self.client().post('/movies', headers={
            "Authorization": f"Bearer {Assistant}"}, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_post_movies_rbac_director(self):
        res = self.client().post('/movies', headers={
            'Authorization': f"Bearer {Director}"}, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_patch_actors(self):
        res = self.client().patch('/actors/1', headers={
            "Authorization": f"Bearer {Director}"}, json={"age": "42"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_actors_422(self):
        res = self.client().patch('/actors/55', headers={
            "Authorization": f"Bearer {Director}"}, json={"age": "42"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable.")

    def test_patch_actors_rbac_assistant(self):
        res = self.client().patch('/actors/1', headers={
            "Authorization": f"Bearer {Assistant}"}, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_patch_movies(self):
        res = self.client().patch('/movies/1', headers={
            "Authorization": f"Bearer {Director}"}, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_movies_422(self):
        res = self.client().patch('/movies/55', headers={
            "Authorization": f"Bearer {Director}"}, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable.")

    def test_patch_movies_rbac_assistant(self):
        res = self.client().patch('/movies/1', headers={
            "Authorization": f"Bearer {Assistant}"}, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_actors(self):
        actor = Actor.query.all()[-1].id
        res = self.client().delete('/actors/' + str(actor), headers={
            "Authorization": f"Bearer {Director}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], actor)

    def test_delete_actors_422(self):
        res = self.client().delete('/actors/55', headers={
            "Authorization": f"Bearer {Director}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable.")

    def test_delete_actors_rbac_assistant(self):
        res = self.client().delete('/actors/1', headers={
            "Authorization": f"Bearer {Assistant}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_movies(self):
        movie = Movie.query.all()[-1].id
        res = self.client().delete('/movies/' + str(movie), headers={
            "Authorization": f"Bearer {Producer}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], movie)

    def test_delete_movie_422(self):
        res = self.client().delete('/movies/55', headers={
            "Authorization": f"Bearer {Producer}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable.")

    def test_delete_movies_rbac_assistant(self):
        res = self.client().delete('/movies/1', headers={
            "Authorization": f"Bearer {Assistant}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_movies_rbac_director(self):
        res = self.client().delete('/movies/1', headers={
            "Authorization": f"Bearer {Director}"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

if __name__ == '__main__':
    unittest.main()
