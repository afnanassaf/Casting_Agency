
import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from unittest.mock import patch


from app import create_app
from models import setup_db, Actor, Movie


EXECUTIVE_PRODUCER_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UckVsTW54aTA5RjJ1YkNXeXpsWCJ9.eyJpc3MiOiJodHRwczovL2FzdGluZy1hZ2VuY3ktZnNuZC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ODI2ZDUyYzM2ZmQwMDY3YzVlZjQzIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5ODcwMjcxNiwiZXhwIjoxNTk4NzA5OTE2LCJhenAiOiJhUTBFSFhPbUZZQXlSVjIxVm9ZTHJxalg5VktmQzF4YiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0OmhvbWUiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.R2dzwKkbI9xK-OVsYUqWnjRXaXhLnh4LsP6KXFsANFelyE2s7uJPuj0A8pNrR5hZDKZ9JkIjSp60WBZIKDzOg0O7kZW3p1uxopZ7mlh2ziC3bpInFuOBwsPLKZH7cpnBjoRkUz7gRH9je31Uj2b92bbhgkGq8kBajWDrupM-Ag1PB8pvKVcXtTdgEIOQ4MH0Tq08MHaXnl49xDpKNhWSHj-AmAx5oP2vCIfx8KERj-x9m_AuaKL8p1qj4Eo36Y_6DYE4tnuli2Dwloi05L3o3qBW-GyJYmILS19-daMSLrTYyJp74pMhIl3P4zEw8TPvkNXJIaVuoz688O1NT5NEmw'
CASTING_ASSISTANT_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UckVsTW54aTA5RjJ1YkNXeXpsWCJ9.eyJpc3MiOiJodHRwczovL2FzdGluZy1hZ2VuY3ktZnNuZC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ODI2ZDUyYzM2ZmQwMDY3YzVlZjQzIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5ODcwNDc1MiwiZXhwIjoxNTk4NzExOTUyLCJhenAiOiJhUTBFSFhPbUZZQXlSVjIxVm9ZTHJxalg5VktmQzF4YiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDpob21lIiwiZ2V0Om1vdmllcyJdfQ.Mue4s8LUF8K_blcWbHF4e2WFk9lQ8YmlNAB_mTr75pJYx3XvbK0SJQi0j8jX42m5KhOJrw7PJ2jzvl-hzcRH4C_qiestwkm37NjAnANpks7240IVAg7Ka45wgw767CL1-hK4JAXMJrKv_gNPJk2U4CRxUxKc3rSyXH7ZgWq9MGXXxjY28RpLJb3iEvCHMUIKTNfee1gRaRnH0QS1dJY5LyQ_Ww5parHv3wrvuhyPJsnU52WPovIlaokQMD9_LTO80-21-d8O55EI5JvvYffuxrP1zgoyjEqlNZskg8z6kBaIwQBeHbHKNKnf_oZc0-Ur7QoYXxzsJ_ltUK021svpUw'
CASTING_DIRECTOR_CREDENTIALS='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UckVsTW54aTA5RjJ1YkNXeXpsWCJ9.eyJpc3MiOiJodHRwczovL2FzdGluZy1hZ2VuY3ktZnNuZC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ODI2ZDUyYzM2ZmQwMDY3YzVlZjQzIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU5ODcwNDQ5MiwiZXhwIjoxNTk4NzExNjkyLCJhenAiOiJhUTBFSFhPbUZZQXlSVjIxVm9ZTHJxalg5VktmQzF4YiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6aG9tZSIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.WMuUgmZIugOPnBMtKBuY_dewrsRKN4Lu3_stWW7kksKtDqsBYVt2LZuOD_BTgp4sV-RBH9edCRdaqyZxX41foz6ZSg9A3J2GNr4PFgg3oREvHxUdIloiGS0iccT9M3HFHBCD5zzvq38EUfME57grUO8Dy-fdyQ1nL0wEPc9d_bKzx8Bo0IW4Uwyxd59vyKq3h6EK7xJOYxzQZjWSqTh8il_LgsPPah-vigId3sAIAUXR9ixtPD73BdOFToL35DNO4wfp7mTBnS8Bzh3yXLdEhcyLHvmOwLjeW0ac842XxGDY5St06Dot7LEu9NVg1Eru37XSUVNeGb1604XaKPKqhw'



class CastingAgencyCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client =self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://postgres:1234567@localhost:5433/casting_agency_test"
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
    
    def tearDown(self):
        pass
  

    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['totalActors'])


    def test_get_actors_not_found(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], false)


    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(data['totalMovies'])


    def test_get_movies_not_found(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_post_actors(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)},
        json={"age": 44,"gender": "Female","name": "Kate Winslet"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(len(data['actors']))


    def test_post_actors_bad_request(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_post_movies(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)}, 
        json={"release_date": "18-11-1997","title": "Titanic"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])
        self.assertTrue(len(data['movie']))


    def test_post_movies_bad_request(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_delete_movies(self):
        res = self.client().post('/movies/1', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(data['totatMovies'])
        self.assertTrue(data['success'], True)


    def test_delete_movies_not_found(self):
        res = self.client().delete('/movies/7000', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(data['success'], True)


    def test_delete_actors_not_found(self):
        res = self.client().delete('/actors/5012', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)


    def test_patch_actors(self):
        res = self.client().patch('/actors/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)},
        json={"name": "Kate Winslet"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['totalActors'])
        self.assertTrue(data['success'], True)


    def test_patch_actors_bad_request(self):
        res = self.client().patch('/actors/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)
    

    def test_patch_movies(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)},
        json={"title": "Titanic"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(data['totalMovies'])
        self.assertTrue(data['success'], True)


    def test_patch_movies_bad_request(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_patch_movies_bad_request(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(EXECUTIVE_PRODUCER_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)


    def test_patch_actors_unauthorized(self):
        res = self.client().patch('/actors/2', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], "unauthorized")
        self.assertEqual(data['success'], False)


    def test_patch_movies_unauthorized(self):
        res = self.client().patch('/movies/2', headers={"Authorization": "Bearer {}".format(CASTING_DIRECTOR_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], "unauthorized")
        self.assertEqual(data['success'], False)


    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(CASTING_ASSISTANT_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertTrue(data['totalActors'])


    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(CASTING_DIRECTOR_CREDENTIALS)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(data['totalMovies'])


if __name__ == "__main__":
    unittest.main()