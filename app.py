import os
from flask import Flask, render_template
from route import *
from scraper import *
from gevent import monkey

monkey.patch_all()

from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import redis

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
#set up SQL alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app)
app._static_folder = os.path.join(os.getcwd(),"static")

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return "username: " + self.username + "\n" + "password: " + self.password

redis_store = redis.Redis(host="0.0.0.0")

@app.route('/')
def index():
	return route_index() 

@app.route('/new_login')
def newlogincheck():
    print("newlogincheck")
    old_len = len(redis_store.lrange('logged_in_users', 0, -1))
    while(len(redis_store.lrange('logged_in_users', 0, -1)) <= old_len):
        if(len(redis_store.lrange('logged_in_users', 0, -1)) < old_len):
            old_len = len(redis_store.lrange('logged_in_users', 0, -1))
        else:
            continue
    print("new guy in",redis_store.lindex('logged_in_users',-1).decode())
    return redis_store.lindex('logged_in_users',-1).decode()

@app.route('/update_logout')
def removefromcontacts():
    print("removefromcontacts")
    old_len = len(redis_store.lrange('logged_in_users', 0, -1))
    old_list = redis_store.lrange('logged_in_users', 0, -1)
    while( len(redis_store.lrange('logged_in_users', 0, -1))>=old_len):
        if(len(redis_store.lrange('logged_in_users', 0, -1))>old_len):
            old_len =len(redis_store.lrange('logged_in_users', 0, -1))
            old_list = redis_store.lrange('logged_in_users', 0, -1)
        else:
            continue
    
    for user in old_list:
        if(user not in redis_store.lrange('logged_in_users', 0, -1)):
            print("logout")
            print(user.decode())
            return user.decode()

    return ""


@app.route('/to_chat')
def chat():
    return render_template('chat.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Register Form
	if request.method == 'POST':
		new_user = User(username=request.form['username'], password=request.form['password'])
		db.session.add(new_user)
		db.session.commit()
		print("done")
		username=request.form['username']
		password=request.form['password']
		data = User.query.filter_by(username=username, password=password).first()
		try:
			data = User.query.filter_by(username=username, password=password).first()
			if data is not None:
                # insert into redis hash name logged in this
                # userame indicating that he is online and available for chatting
                # Add the username to the session
				session["username"] = username
				redis_store.rpush("logged_in_users", username)
				
				return redirect(url_for("start_chat"))
			else:
				print('Wrong Details')
				return render_template("register.html") 
		except:
			return "Dont Login"
	else:
		return render_template("register.html")    

@app.route('/login', methods = ["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    else:
        # login logic
        username = request.form['username']
        password = request.form['password']
        try:
            data = User.query.filter_by(username=username, password=password).first()
            if data is not None:
                # insert into redis hash name logged in this
                # userame indicating that he is online and available for chatting

                # Add the username to the session
                session["username"] = username

                redis_store.rpush("logged_in_users", username)
                
                return redirect(url_for("start_chat"))
            else:
                print('Wrong Details')
                return redirect(url_for('register'))
        except:
            return "Dont Login"


@app.route("/logout", methods = ["GET"])
def logout():

    try:
        session["username"]
    except:
        return "404!!! First Login then logout Monjjunath!!"

    username = session['username']
    
    # clear session
    session['username'] = ''

    # remove from redis
    redis_store.lrem("logged_in_users", username)

    return redirect(url_for("index"))

@app.route('/data')
def get_session():

    return "session['username']: " +  str(session['username']) + '\n' + "logged_in_users: " + str(redis_store.lrange('logged_in_users', 0, -1))

@app.route("/start_chat", methods = ["GET"])
def start_chat():
    try:
        session["username"]
    except:
        return redirect(url_for("login"))

    if session["username"]:
        list_of_users = []
        
        for user in redis_store.lrange('logged_in_users', 0, -1):
            if(session['username'] != user.decode()):
                list_of_users.append(user.decode())

        return render_template("pretty_chat.html", users = list_of_users)
    else:
        return redirect(url_for("login"))


@socketio.on('message', namespace='/chat')
def chat_message(message):
    message['from'] = session['username']
    print('chat_message: ', message)
    emit('message', message, broadcast = True, room = redis_store.hget("chat_room", message['to']).decode())

@socketio.on('connect', namespace='/chat')
def test_connect():
    print("connect")
    emit('my response', {'data': 'Connected', 'count': 0})

@socketio.on('my_connection', namespace='/chat')
def my_connection(data):
    # add mapping of username and request.sid to redis
    # name of the hash:  
    # chat_room

    redis_store.hset("chat_room", session["username"], request.sid)
    print('my_connection')
    print(data)

@app.route('/results', methods=["POST"])
def results():
	return route_result()

@app.route('/depression_questions', methods=["GET"])
def depression_questions():
	#Your mind will take the shape of what you frequently hold in thought,
	# for the human spirit is colored by such impressions.
	
	# question_list = []

	# for i in range(2,29):
	# 	url = "https://www.quizony.com/what-emotion-are-you-feeling-right-now/"+str(i)+".html"
	# 	q = scrape_display(url)
	# 	question_list.append(q)

	# print(question_list)
	question_list = [['How easy is it to talk about your feelings?', "It's difficult or impossible.", "I don't have anyone to talk to.", "Some feelings are hard to talk about, but I do it because I know it's healthy to talk things out.", "I don't trust anyone so I have a hard time opening up to others."], ['Do you have a pet?', 'Yes.', 'Yes, the best pet ever.', 'No.', 'No, I hate animals.'], ['How much time do you spend on social media?', 'None or very little', 'An hour or so. I like to keep my friends posted and see what they are up to.', 'Hours and hours!'], ['How fast is your heart beating right now?', 'Super fast.', 'Normal speed, I guess.', 'Slow, barely keeping me alive.'], ['Do you have high blood pressure?', 'Yes.', "I don't know.", 'No.'], ['Did something negative happen today? (Examples: a break-up, missed flight, injury, etc.)', 'I woke up.', 'No, today has been great so far!', 'Yes.', "No, but the day's not over yet!", "Yes, and it wasn't fair!"], ['What would you do during a traffic jam?', 'Honk my horn and give people the finger.', 'Keep checking my watch and calculating how many minutes I have left to arrive on time.', 'Put my favorite song on repeat and try to memorize the words while I drum the beat on the steering wheel.', 'Check my phone for new messages.', 'Rev my engine and wink at other drivers.', "Just sit there and endure it until it's over."], ['Fight or flight?', 'Fight', 'Flight'], ["How do you stand when you are talking to someone you don't know well?", 'Arms at my side, hands in fists', 'Arms crossed across my chest or stomach', 'Shifting weight from one leg to the other or fidgeting with something', 'Hands on hips', 'Head down, eyes lowered', 'Straight with hands hanging casually down at my sides'], ['Are you an introvert or an extrovert?', 'Extrovert', 'Depends', 'Introvert'], ['Who lives with you?', 'No one', 'My family', 'Roommate(s)'], ['Do you enjoy spending time alone?', 'Occasionally', 'Yes, I prefer it.', "No I don't like it."], ['When is the last time you helped someone?', "I don't remember.", 'Recently', 'A long time ago'], ['Have you sung a song aloud today?', 'Yes.', 'Nope.'], ['Yesterday at this time, were you feeling the same emotion that you feel right now?', 'Yes.', 'No.'], ['What would you want on your shelf in your living room?', 'A bottle of alcohol', 'A trophy', 'A fish bowl', 'A bouquet of flowers', 'A candle', 'A voodoo doll'], ['Which activity would you most likely do in your spare time?', 'Binge watching TV series', 'Taking selfies', 'Reading', 'Doing a craft project', 'Talking to yourself', 'Looking out of the window every time ou hear a noise'], ['Are you better than most people?', 'Yes.', "I'm the worst.", 'I am proud of who I am, but I know there are many others in the world who are more awesome than I am!', "I'm better than all the people."], ['How often do you get offended?', 'Every day', 'Rarely', 'Occasionally'], ['How much do you eat?', "I diet a lot because I'm afraid of getting fat.", 'I eat reasonable portions with regular treats.', 'I barely eat or I eat everything in sight.', 'I eat perfect portions.'], ['Do you have trouble concentrating?', 'Yes.', 'No.', 'Sometimes.'], ['Where do you experience the most problems?', 'At home', 'At work', 'At school'], ['Who is usually right?', 'Depends.', 'Me.', 'The other person'], ['One of your friends appears to be avoiding you. What do you do?', 'Cry.', "Ask them what's wrong.", "Assume they don't want to be your friend anymore.", 'Avoid them.', 'Talk about them behind their backs.'], ['What do you say when you are wrong?', 'Sorry.', 'Nothing.', 'You probably hate me now. . .'], ['Are you sweaty now?', "How did you know I haven't taken a shower today?", "Yes, but it's because I just finished working out.", 'Sweaty and stinky!', 'Yes; I have no idea why.', 'How dare you ask such a thing?'], ['Turn off the lights. What does the first shape look like?', 'A homicidal maniac', 'My ex', 'A bunny', 'A robot', 'A car', 'A donkey']]
	
	#print(question_list)
	return route_question(question_list[:6])


@app.route('/get_depr_results', methods=["GET","POST"])
def get_depr_results():
	answers = request.args.get('array')
	return route_depr_results(answers)




if (__name__ == "__main__"):
    db.create_all()
    socketio.run(app, host="0.0.0.0", debug=True)
