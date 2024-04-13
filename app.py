from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pymysql
import cryptography
import config
# create an instance of the Flask class
# __name__ = name of the module
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.username}:{config.password}@{config.hostname}:{config.port}/{config.database}?charset=utf8mb4'

# connect to the database
db = SQLAlchemy(app)
# test connection

with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text('SELECT 1'))
        print(rs.fetchone())

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)




# route() decorator to tell Flask what URL should trigger our function
@app.route('/')
def hello_world():  # put application's code here
    user = User(username='John', email='123@gmail.com')
    person={
        'username': 'Jason',
        'email': 'abc@gmail.com'
    }
    return render_template("index.html", user=user, person=person)

@app.route('/filter')
def filter_demo():
    user = User(username='John', email='123@gmail.com')
    return render_template("filter.html", user=user)

@app.route('/profile')
def profile():
    return 'Profile'


@app.route('/profile/<username>')
def profile_username(username):
    return render_template("profile_username.html", username=username, id=2)


@app.route('/book/list')
def book_list():
    page = request.args.get('page', 1, int)
    return f"now is {page}"

@app.route('/control')
def control_statement():
    age=19
    books =[{
        "name":"book1",
        "price":100
    },{
        "name":"book2",
        "price":200
    },{
        "name":"book3",
        "price":300
    }]
    return render_template("control.html",age=age, books=books)

@app.route('/child')
def child():
    return render_template("child.html")


@app.route('/static')
def static_demo():
    return render_template("static.html")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
