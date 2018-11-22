import os
from flask import Flask, render_template
from route import *
from scraper import *
app = Flask(__name__)
app._static_folder = os.path.join(os.getcwd(),"static")

@app.route('/')
def index():
	return route_index() 

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
    app.run(debug=True)