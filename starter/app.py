import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Movie, Actor, database_path
from auth import AuthError, requires_auth



ITEMS_PER_PAGE = 10


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response



  @app.route('/home')
  def get_home():
     return  jsonify({'message':'Welcome To Casting Agency' })



  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors():
     page =  request.args.get('page', 1, type=int)
     start = (page - 1 ) * ITEMS_PER_PAGE
     end = start + ITEMS_PER_PAGE
     actors=Actor.query.all()
     formatted_actors = [ actor.format() for actor in actors ]
     selection = formatted_actors[start:end]

     if len(selection) == 0:
        abort(404)

     return  jsonify({'actors':selection, 'totalActors':len(formatted_actors) })


  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies():
     page =  request.args.get('page', 1, type=int)
     start = (page - 1 ) * ITEMS_PER_PAGE
     end = start + ITEMS_PER_PAGE
     movies=Movie.query.all()
     formatted_movies = [ movie.format() for movie in movies ]
     selection = formatted_movies[start:end]

     if (len(selection) == 0):
        abort(404)

     return  jsonify({'movies':selection, 'totalMovies':len(formatted_movies)})


  @app.route('/actors',  methods=['POST'])
  @requires_auth('post:actors')
  @cross_origin()
  def create_actor():
      body = request.get_json(force=True)

      if  body==None :
         abort(422)

      new_age = body.get('age', None)
      new_gender = body.get('gender', None)
      new_name = body.get('name', None)
      new_id = body.get('id', None)

      try:
        actor = Actor (age=new_age, gender=new_gender, name=new_name )
        actor.insert()

        selection = Actor.query.order_by(Actor.id).all()
        page =  request.args.get('page', 1, type=int)
        start = (page - 1 ) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        current_actors = selection[start:end]
        formatted_actors = [ actor.format() for actor in current_actors ]
         
        return  jsonify({'success':True, 'actors':formatted_actors,'totalActors':len(formatted_actors)})    
      except:
       abort(422)



  @app.route('/movies',  methods=['POST'])
  @requires_auth('post:movies')
  @cross_origin()
  def create_movie():
      body = request.get_json(force=True)

      if  body==None :
         abort(422)

      new_title = body.get('title', None)
      new_release_date = body.get('release_date', None)

      try:
        movie = Movie (title=new_title, release_date=new_release_date )
        movie.insert()
        
        selection = Movie.query.order_by(Movie.id).all()
        page =  request.args.get('page', 1, type=int)
        start = (page - 1 ) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        current_movies = selection[start:end]
        formatted_movies = [ movie.format() for movie in current_movies ]
         
        return  jsonify({'success':True, 'movie':formatted_movies,'totalMovies':len(formatted_movies)}) 
      except:
         abort(422)   
  


  @app.route('/actors/<int:actor_id>',  methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actor(actor_id):

      body = request.get_json(force=True)
      if  body==None :
         abort(422)

      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
         abort(404)

      new_age = body.get('age', None)
      new_gender = body.get('gender', None)
      new_name = body.get('name', None)
    
      try:
        if actor is not None:
          actor.age=new_age
        if actor is not None:
          actor.gender=new_gender
        if actor is not None:
          actor.name=new_name
          
        actor.update()

        selection = Actor.query.order_by(Actor.id).all()
        page =  request.args.get('page', 1, type=int)
        start = (page - 1 ) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        current_actors = selection[start:end]
        formatted_actors = [ actor.format() for actor in current_actors ]
         
        return  jsonify({'success':True, 'actors':formatted_actors,'totalActors':len(formatted_actors)})    
      except:
       abort(422)


  @app.route('/movies/<int:movie_id>',  methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movie(movie_id):

      body = request.get_json(force=True)
      if  body==None :
         abort(422)

      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if actor is None:
         abort(404)

      new_title = body.get('title', None)
      new_release_date = body.get('release_date', None)

      try:
        if movie is not None:
          movie.title=new_title
        if movie is not None:
          movie.release_date=new_release_date

        movie.update()

        selection = Movie.query.order_by(Movie.id).all()
        page =  request.args.get('page', 1, type=int)
        start = (page - 1 ) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        current_movies = selection[start:end]
        formatted_movies = [ movie.format() for movie in current_movies ]
         
        return  jsonify({'success':True, 'movies':formatted_actors,'totalMovies':len(formatted_movies)})    
      except:
       abort(422)


  @app.route('/actors/<int:actor_id>',  methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(actor_id):

      actor = Actor.query.filter(Movie.id == actor_id).one_or_none()

      if actor is None:
         abort(404)

      actor.delete()
      actors = Actor.query.order_by(Actor.id).all()
      formatted_actors = [ actors.format() for actor in actors]

      if len(formatted_actors) == 0 :
          abort(404)

      return  jsonify({'success':True, 'actors':formatted_actors, 'totalActors':len(formatted_actors)})


  @app.route('/movies/<int:movie_id>',  methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(movie_id):

      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
         abort(404)

      movie.delete()
      movies = Movie.query.order_by(Movie.id).all()
      formatted_movies = [ movie.format() for movie in movies]

      if len(formatted_movies) == 0 :
          abort(404)

      return  jsonify({'success':True, 'movies':formatted_movies, 'totalMovies':len(formatted_movies)})



  @app.errorhandler(400)
  def bad_request(error):
     return   jsonify({'success':False, 'error':400,'message':'bad request'})


  @app.errorhandler(404)
  def not_found(error):
     return   jsonify({'success':False, 'error':404,'message':'resource not found'})


  @app.errorhandler(422)
  def unprossable_entity(error):
     return   jsonify({'success':False, 'error':422,'message':'unprossable entity'})

   
  @app.errorhandler(500)
  def internal_error(error):
     return   jsonify({'success':False, 'error':500,'message':'internal server error'})


  @app.errorhandler(403)
  def internal_error(error):
     return   jsonify({'success':False, 'error':403,'message':'forbidden'})


  @app.errorhandler(401)
  def internal_error(error):
     return   jsonify({'success':False, 'error':401,'message':'unauthorized'})



  return app

app = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)


