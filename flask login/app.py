
from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from instagram import getfollowedby, getname


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_new.db'
db = SQLAlchemy(app)


class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email=db.Column(db.String(80),unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username,email, password):
		self.username = username
		self.email=email
		self.password = password

'''
@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')
	'''


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = User.query.filter_by(username=name, password=passw).first()
			if data is not None:
				return "logged in"
			else:
				print('Wrong Details')
				return redirect(url_for('register'))
		except:
			return "Dont Login"

@app.route('/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		new_user = User(username=request.form['username'], email=request.form['email'],password=request.form['password'])
		db.session.add(new_user)
		db.session.commit()
		print("done")
		return render_template('login.html')
	return render_template('index.html')




if __name__ == '__main__':
	app.debug = True
	db.create_all()
	app.secret_key = "123"
	app.run(host='0.0.0.0')
	