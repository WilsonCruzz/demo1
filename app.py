from flask import Flask, request

#create an instance of the Flask class
#__name__ = name of the module
app = Flask(__name__)


#route() decorator to tell Flask what URL should trigger our function
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/profile')
def profile():
    return 'Profile'

@app.route('/profile/<username>')
def profile_username(username):
    return 'Profile: ' + username

@app.route('/book/list')
def book_list():
    page = request.args.get('page', 1, int)
    return f"now is {page}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
