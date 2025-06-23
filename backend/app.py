from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.bookreviewdb
books_collection = db.books


def serialize_book(book):
    book['_id'] = str(book['_id'])
    return book


@app.route('/api/books', methods=['GET'])
def get_books():
    books = list(books_collection.find())
    return jsonify([serialize_book(book) for book in books])


@app.route('/api/book/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = books_collection.find_one({"_id": ObjectId(book_id)})
    except:
        return jsonify({"error": "Invalid book ID"}), 400
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(serialize_book(book))


@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    book = {
        "title": data.get('title'),
        "author": data.get('author'),
        "description": data.get('description', ''),
        "reviews": []
    }
    result = books_collection.insert_one(book)
    book['_id'] = str(result.inserted_id)
    return jsonify(book), 201


@app.route('/api/book/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = books_collection.delete_one({'_id': ObjectId(book_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Book deleted'}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404


@app.route('/api/book/<book_id>/review', methods=['POST'])
def add_review(book_id):
    data = request.json
    review = {
        "reviewer": data.get('reviewer'),
        "text": data.get('text'),
        "rating": data.get('rating')
    }
    try:
        result = books_collection.update_one(
            {"_id": ObjectId(book_id)},
            {"$push": {"reviews": review}}
        )
    except:
        return jsonify({"error": "Invalid book ID"}), 400
    if result.matched_count == 0:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(review), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
