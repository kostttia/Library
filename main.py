from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from wtforms.validators import DataRequired
import datetime

todays_date = datetime.date.today()

class MyForm(FlaskForm):
    rating = StringField("New Rating", validators=[DataRequired()])
    submit = SubmitField("Submit")

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = 'your_secret_key_here'
@app.route('/')
def home():
    books = db.session.query(Book).all()
    num_of_books = len(books)
    return render_template("index.html", date=todays_date, num_of_books=num_of_books)

@app.route('/library')
def library():
    books = db.session.query(Book).all()
    return render_template("library.html", books=books)

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    my_form = MyForm()
    book_to_update = db.get_or_404(Book, book_id)

    if my_form.validate_on_submit():
        book_to_update.rating = float(my_form.rating.data)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", book=book_to_update, form=my_form)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        bookname = request.form['bookname']
        author = request.form['author']
        rating = request.form['rating']
        new_book = {
            'title':bookname,
            'author':author,
            'rating':rating
        }
        with app.app_context():
            new_book = Book(title=new_book['title'], author=new_book['author'], rating=new_book['rating'])
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(model_class=Base)

db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

