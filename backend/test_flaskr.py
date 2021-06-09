"Import rquirements"
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book

class ResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'test_db'
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'pysql','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            "title": "Alvido bolalik",
            "author": "Tohir Malik",
            "rating": "6"
        }

        self.another_book = {
            "title": "Testing",
            "rating": "6"
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()
    
    def tearDown(self):
        'Executed after all tests'
        pass

    def test_get_paginated_books(self):
        "Checking response of API to getting all books"
        response = self.client().get('/books')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])
        self.assertEqual(data['success'], True)
    
    def test_for_404_error(self):
        response = self.client().get('/books/lorem')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_404_resource(self):
        "Checking response the API for 404 error"
        response = self.client().get('/books?page=10000')
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'books not found')

    def test_get_single_book(self):
        "Get book with ID"
        book = Book.query.first().id
        response = self.client().get(f'/books/{book}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['author'])
        self.assertTrue(data['rating'])

    def test_get_failed_single_book(self):
        response = self.client().get('/books/10000')
        data = json.loads(response.data)
        book = Book.query.get(10000)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'books not found')
        self.assertIsNone(book)

    def test_update_book(self):
        "Checking update for endpoint"
        single_book = Book.query.first().id
        response = self.client().patch(f'/books/{single_book}', json={'rating': 1})
        data = json.loads(response.data)
        book = Book.query.get(data['id'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertEqual(book.format()['rating'], 1)

    def test_400_for_failed_update(self):
        response = self.client().patch('/books/1111', json={'rating': 8})
        data = json.loads(response.data)
        book = Book.query.get(1111)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertIsNone(book)

    def test_search_book(self):
        response = self.client().post('/books/search', json={'search': 'alvido'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])

    def test_search_book_failed(self):
        response = self.client().post('/books/search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')


    def test_delete_book(self):
        last = Book.query.all()[-1].id
        response = self.client().delete(f'/books/{last}')

        data = json.loads(response.data)

        book = Book.query.filter(Book.id == last).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], last)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
        self.assertIsNone(book)

    def test_delete_book_failed(self):
        response = self.client().delete(f'books/122222')
        data = json.loads(response.data)

        book = Book.query.filter(Book.id == 122222).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'deleting was unseccussful')
        self.assertIsNone(book)

    def test_create_book(self):
        response = self.client().post('/books', json=self.new_book)
        data = json.loads(response.data)
        book = Book.query.get(data['created'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.id, data['created'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])
        self.assertTrue(book.rating)

    def test_create_book_for_method_not_allowed(self):
        response = self.client().post('/books/1', json=self.another_book)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

if __name__ == '__main__':
    unittest.main()