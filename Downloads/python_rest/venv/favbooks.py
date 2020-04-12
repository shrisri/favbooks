from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps


app = Flask(__name__)  # Creating instance of Flask

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# Creating 2 models for Users and FavBooks table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))


class FavBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer)
    title = db.Column(db.String(50),nullable=False)
    amazon_url = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)


db.create_all()  # Creating the 2 tables


# Function to check if token user entered is valid
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:  # Checking is token is entered by user
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])  # Decoding token using secret key
            current_user = Users.query.filter_by(public_id=data['public_id']).first()  # Searching for current user detaild using decoded token
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


# Function signup_user() to get name and password from user and add to Users database
@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')  # Generating hashed password

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)  # Creating instance of Users class (new_user)
    db.session.add(new_user)  # Adding new_user to Users database
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


# Function login_user() to check if login credentials are valid and generate a random JWT token
@app.route('/login', methods=['GET', 'POST'])
def login_user():

    auth = request.authorization  # Reading user's login details

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):  # Checking if password entered is valid
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  # Encoding public_id to generate random token
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


# Function get_all_users() to get information of all users that have registered from Users database
@app.route('/users', methods=['GET'])
def get_all_users():

    users = Users.query.all()  # Getting all data from Users database

    result = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password

        result.append(user_data)

    return jsonify({'users': result})



# Function add_fav() to add a new favourite book to user's list of favourite books
@app.route('/addfav', methods=['POST', 'GET'])
@token_required
def add_fav(current_user):

    data = request.get_json()  # Reading user entered data of favourite book

    new_fav = FavBooks(user_id=current_user.id,title=data['title'], amazon_url=data['amazon_url'], author=data['author'], genre=data['genre'])  # Creating instance of FavBooks class
    db.session.add(new_fav)  # Adding new favourite book to FavBooks database
    db.session.commit()

    return jsonify({'message' : 'new favourite book added'})


# Function get_fav() to get all favourite books of the current user logged in
@app.route('/favbooks', methods=['POST', 'GET'])
@token_required
def get_fav(current_user):

    books = FavBooks.query.filter_by(user_id=current_user.id).all()  # Getting all favourite books from FavBooks database

    output = []
    for book in books:
        book_data = {}
        book_data['title'] = book.title
        book_data['amazon_url'] = book.amazon_url
        book_data['author'] = book.author
        book_data['genre'] = book.genre
        book_data['id']=book.id
        output.append(book_data)

    return jsonify({'your favorite books' : output})


# Function delete_fav() to delete a particular favourite book from user's list
@app.route('/favbooks/<book_id>', methods=['DELETE'])
@token_required
def delete_fav(current_user, book_id):
    book = FavBooks.query.filter_by(id=book_id, user_id=current_user.id).first()  # Searching for favourite book with id=book_id
    if not book:
        return jsonify({'message': 'book does not exist'})


    db.session.delete(book)  # Deleting book with id=book_id
    db.session.commit()

    return jsonify({'message': 'Book deleted'})


# Function update_fav() to change details of any book in list of user's favourite books
@app.route('/favbooks/<book_id>', methods=['PUT'])
@token_required
def update_fav(current_user, book_id):
    data = request.get_json()  # Reading user's updated book data

    book = FavBooks.query.filter_by(id=book_id, user_id=current_user.id).first()  # Searching for favourite book with id=book_id
    if not book:
        return jsonify({'message': 'book does not exist'})

    # Updating all information of the favourite book with id=book_id
    book.title=data['title']
    book.amazon_url=data['amazon_url']
    book.author=data['author']
    book.genre=data['genre']
    book.id=book_id
    book.user_id=current_user.id
    db.session.commit()

    return jsonify({'message': 'Book updated'})




if  __name__ == '__main__': 
     app.run(debug=True)



