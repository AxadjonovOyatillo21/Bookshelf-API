import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * BOOKS_PER_SHELF
  end = start + BOOKS_PER_SHELF
  books = [book.format() for book in selection]
  current_books = books[start:end]

  return current_books

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  @app.route('/books', methods=['GET'])
  def get_books():
    selection = Book.query.order_by(Book.id).all()
    current_books = paginate_books(request, selection)
    if len(current_books) > 0:
      return jsonify({
        'success': 'True',
        'books': current_books,
        'total_books': len(Book.query.all())
      })
    else:
      abort(404)
     
  @app.route('/books/search', methods=['POST'])
  def search_books():
    search_term = request.get_json()['search']
    selection = Book.query.filter(Book.title.ilike(f'%{search_term}%'))
    current_books = paginate_books(request, selection)
    return jsonify({
      'success': 'True',
      'books': current_books,
      'total_books': len(Book.query.all())
    })

  @app.route('/books/<int:book_id>', methods=['GET'])
  def retrive_book(book_id):

    try:
      book = Book.query.get_or_404(book_id)
      if book is None:
        abort(404)
      return jsonify({
        'success': 'True',
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'rating': book.rating
      })
    except:
      abort(400)

  @app.route('/books/<int:book_id>', methods=['PATCH'])
  def update_book(book_id):

    data = request.get_json()

    try:
      book = Book.query.filter_by(id=book_id).one_or_none()
      if book is None:
        abort(404)
      if 'rating' in data:
        book.rating = int(data['rating']) 
      if 'title' in data:
        book.title = data['title']
      if 'author' in data:
        book.author = data['author']
     
      book.update()

      return jsonify({
        'success': 'True',
        'id': book.id
      })
    except:
      abort(400)


  @app.route('/books/<int:book_id>', methods=['DELETE'])
  def delete_book(book_id):
    try:
      book = Book.query.get_or_404(book_id)
      book.delete()
      selection = Book.query.order_by(Book.id).all()
      current_books = paginate_books(request, selection)

      return jsonify({
        'success': 'True',
        'deleted': book.id,
        'books': current_books,
        'total_books': len(Book.query.all())
      })
    except:
      abort(400)


  @app.route('/books', methods=['POST'])
  def create_book():

    data = request.get_json()
    new_title = data.get('title')
    new_author = data.get('author')
    new_rating = data.get('rating')

    try:
      new_book = Book(title=new_title, author=new_author, rating=new_rating)
      new_book.insert()
      selection = Book.query.order_by(Book.id).all()
      current_books = paginate_books(request, selection)

      return jsonify({
        'success': 'True',
        'created': new_book.id, 
        'books': current_books,
        'total_books': len(Book.query.all())
      })
    except:
      abort(400)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': 'False',
      'error': 404,
      'message': 'Resource Not found' 
    }), 404
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': 'False',
      'error': 400,
      'message': 'Bad request' 
    }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': 'False',
      'error': 405,
      'message': 'Method not allowed' 
    }), 405

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success': 'False',
      'error': 422,
      'message': 'Unprocessable Entity' 
    }), 422

  return app

    
