from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pymysql
import cryptography
import config
from flask_migrate import Migrate

# create an instance of the Flask class
# __name__ = name of the module
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.username}:{config.password}@{config.hostname}:{config.port}/{config.database}?charset=utf8mb4'

# connect to the database
db = SQLAlchemy(app)
# test connection

migrate = Migrate(app, db)

# 1. flask db init
# 2. flask db migrate : recognize the changes
# 3. flask db upgrade : apply the changes to the database


with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text('SELECT 1'))
        print(rs.fetchone())

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #backref: define the relationship from the User model to the Article model
    author = db.relationship('User', backref='articles')





# with app.app_context():
#     db.create_all()

@app.route('/article/query')
def query_article():
    user = User.query.get(1)
    for article in user.articles:
        print(f'{article.id}:{article.title}')
    return 'query article success'




@app.route('/article/add')
def add_article():
    article1 = Article(title='title1', content='content1')
    article1.author= User.query.get(1)

    article2 = Article(title='title2', content='flask is good')
    article2.author= User.query.get(3)

    db.session.add_all([article1, article2])
    db.session.commit()
    return 'add article success'

# route() decorator to tell Flask what URL should trigger our function
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/user/add')
def add_user():
    # create a new orm object
    user = User(username='Jason', password='123')
    # add the object to the session
    db.session.add(user)
    # commit the session to the database
    db.session.commit()
    return 'add user success'

@app.route('/user/query')
def query_user():
    # 1. get search based on primary key
    # user=User.query.get(1)
    # print(f'{user.id}:{user.username}--{user.password}')
    # 2. get search based on filter
    users=User.query.filter_by(username='John')
    for user in users:
        print(f'{user.id}:{user.username}')
    return 'query user success'

@app.route('/user/update')
def update_user():
    user = User.query.filter_by(username='john').first()
    user.password='222'
    db.session.commit()
    return 'update user success'

@app.route('/user/delete')
def delete_user():
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return 'delete user success'
'''
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

'''
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
