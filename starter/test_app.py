
import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request

from flaskr import create_app
from models import setup_db, Question, Category


class CastingAgencyCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://postgres:1234567@localhost:5433/casting_agency_test"
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()
    
    def tearDown(self):
        pass



    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])
        self.assertTrue(data['id'])
        self.assertTrue(data['name'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(len(data['actors']))


    def test_get_actors_not_found(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 404)
        self.assertEqual(res.data['message'], "resource not found")
        self.assertEqual(data['success'], false)


    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['id'])
        self.assertTrue(data['release_date'])
        self.assertTrue(data['title'])
        self.assertTrue(data['totatMovies'])
        self.assertTrue(len(data['movies']))


    def test_get_movies_not_found(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 404)
        self.assertEqual(res.data['message'], "resource not found")
        self.assertEqual(data['success'], false)


    def test_post_actors(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])
        self.assertTrue(data['id'])
        self.assertTrue(data['name'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(len(data['actors']))


    def test_post_actors_bad_request(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 400)
        self.assertEqual(res.data['message'], "bad request")
        self.assertEqual(data['success'], false)


    def test_post_movies(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['title'])
        self.assertTrue(data['release_date'])
        self.assertTrue(data['id'])
        self.assertTrue(data['totalMovies'])
        self.assertTrue(len(data['movies']))


    def test_post_movies_bad_request(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 400)
        self.assertEqual(res.data['message'], "bad request")
        self.assertEqual(data['success'], false)


    def test_delete_movies(self):
        res = self.client().post('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['id'])
        self.assertTrue(data['release_date'])
        self.assertTrue(data['title'])
        self.assertTrue(data['totatMovies'])
        self.assertTrue(len(data['movies']))


   def test_delete_movies_not_found(self):
        res = self.client().delete('/movies/7000')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 404)
        self.assertEqual(res.data['message'], "resource not found")
        self.assertEqual(data['success'], false)


    def test_delete_actors(self):
        res = self.client().post('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])
        self.assertTrue(data['id'])
        self.assertTrue(data['name'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(len(data['actors']))


   def test_delete_actors_not_found(self):
        res = self.client().delete('/actors/5012')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 404)
        self.assertEqual(res.data['message'], "resource not found")
        self.assertEqual(data['success'], false)


    def test_patch_actors(self):
        res = self.client().patch('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])
        self.assertTrue(data['id'])
        self.assertTrue(data['name'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(len(data['actors']))


   def test_patch_actors_bad_request(self):
        res = self.client().patch('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 400)
        self.assertEqual(res.data['message'], "bad request")
        self.assertEqual(data['success'], false)
    

    def test_patch_movies(self):
        res = self.client().patch('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])
        self.assertTrue(data['id'])
        self.assertTrue(data['name'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(len(data['actors']))


   def test_patch_movies_bad_request(self):
        res = self.client().patch('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.data['error'], 400)
        self.assertEqual(res.data['message'], "bad request")
        self.assertEqual(data['success'], false)


   def test_patch_movies_bad_request(self):
        res = self.client().patch('/movies/2')
        data = json.loads(res.header)

        request.headers.get('Authorization')

        self.assertEqual(res.data['error'], 400)
        self.assertEqual(res.data['message'], "bad request")
        self.assertEqual(data['success'], false)



if __name__ == "__main__":
    unittest.main()