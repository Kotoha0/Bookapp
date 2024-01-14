from flask import render_template, request, redirect, url_for
from flaskr import app
import sqlite3
import random
import string
DATABASE = 'database.db'


@app.route('/')
def index():
    con=sqlite3.connect(DATABASE)
    db_books = con.execute('SELECT*FROM books').fetchall()
    con.close()

    books = []
    for row in db_books:
        books.append({
            'title': row[0],
            'price': row[1],
            'arrival_day': row[2],
            'color': row[3]
        })

    return render_template(
        'index.html',
        books=books
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
    con.execute('INSERT INTO books VALUES(?,?,?,?)',
                [title, price, arrival_day, color])
    con.commit()
    con.close()
    return redirect(url_for('index'))

