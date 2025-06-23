from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL")


@app.route('/')
def index():
    books = requests.get(f"{BACKEND_URL}/api/books").json()
    return render_template('index.html', books=books)


@app.route('/book/<book_id>')
def book_detail(book_id):
    book = requests.get(f"{BACKEND_URL}/api/book/{book_id}").json()
    return render_template('book_detail.html', book=book)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        data = {
            "title": request.form['title'],
            "author": request.form['author'],
            "description": request.form['description']
        }
        requests.post(f"{BACKEND_URL}/api/books", json=data)
        return redirect(url_for('index'))
    return render_template('add_book.html')


@app.route('/delete/<book_id>', methods=['POST'])
def delete_book(book_id):
    requests.delete(f"{BACKEND_URL}/api/book/{book_id}")
    return redirect(url_for('index'))


@app.route('/book/<book_id>/add_review', methods=['GET', 'POST'])
def add_review(book_id):
    if request.method == 'POST':
        data = {
            "reviewer": request.form['reviewer'],
            "rating": int(request.form['rating']),
            "text": request.form['text']
        }
        requests.post(f"{BACKEND_URL}/api/book/{book_id}/review", json=data)
        return redirect(url_for('book_detail', book_id=book_id))
    # GET request: load book info to display title on the form
    book = requests.get(f"{BACKEND_URL}/api/book/{book_id}").json()
    return render_template('add_review.html', book=book)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
