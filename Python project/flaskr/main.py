from flask import render_template, request, redirect, url_for
from flaskr import app
import sqlite3
import random
import string
from datetime import date, timedelta
DATABASE = 'database.db'


@app.route('/')
def index():
    search_query = request.args.get('search','')
    if search_query:
        return search_books(search_query)
    else:
        return show_books()


def show_books():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT * FROM books').fetchall()
    con.close()

    books = []
    for row in db_books:
        books.append({
            'title': row[0],
            'price': row[1],
            'arrival_day': row[2],
            'color': row[3],
            'rented_until': row[4]
        })

    return render_template(
        'index.html',
        books=books,
        search_query=''
    )

def search_books(search_query):
    con = sqlite3.connect(DATABASE)
    query = 'SELECT * FROM books WHERE title LIKE ?'
    db_books = con.execute(query, ('%' + search_query + '%',)).fetchall()
    con.close()

    books = [{'title': row[0], 'price': row[1], 'arrival_day': row[2], 'color': row[3]} for row in db_books]

    return render_template(
        'index.html',
        books=books,
        search_query=search_query
    )


@app.route('/form')
def form():
    return render_template('form.html')

def generate_color():
    return '#'+ ''.join(random.choice(string.hexdigits) for _ in range(6))

@app.route('/register', methods=['POST'])
def register():
    title=request.form['title']
    price=request.form['price']
    arrival_day=request.form['arrival_day']
    color = generate_color()


    con=sqlite3.connect(DATABASE)
    con.execute('INSERT INTO books VALUES(?,?,?,?,NULL)',
                [title, price, arrival_day, color])
    con.commit()
    con.close()
    return redirect(url_for('index'))


@app.route('/rent/<title>', methods=['POST'])
def rent_book(title):
    con = sqlite3.connect(DATABASE)
    rented_until = date.today() + timedelta(days=14)
    con.execute('UPDATE books SET rented_until=? WHERE title=?', [rented_until, title])
    con.commit()
    con.close()
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def return_book():
    returned_book = request.form['book']

    con = sqlite3.connect(DATABASE)
    con.execute('UPDATE books SET rented_until=NULL WHERE title=?', [returned_book])
    con.commit()
    con.close()

    return redirect(url_for('index'))

@app.route('/return_form')
def return_form():
    con = sqlite3.connect(DATABASE)
    rented_books = con.execute('SELECT title FROM books WHERE rented_until IS NOT NULL').fetchall()
    con.close()

    return render_template('return_form.html', rented_books=rented_books)

@app.route('/delete_book')
def delete_book():
    con = sqlite3.connect(DATABASE)
    all_books = con.execute('SELECT title FROM books').fetchall()
    con.close()

    return render_template('delete_form.html', all_books=all_books)

@app.route('/delete_confirm', methods=['POST'])
def delete_confirm():
    deleted_book = request.form['book']

    con = sqlite3.connect(DATABASE)
    con.execute('DELETE FROM books WHERE title=?', [deleted_book])
    con.commit()
    con.close()

    return redirect(url_for('index'))
