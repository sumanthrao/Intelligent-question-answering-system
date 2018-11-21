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
def get_questions():
	#Your mind will take the shape of what you frequently hold in thought,
	# for the human spirit is colored by such impressions.
	
	question_list = []

	for i in range(1,29):
		url = "https://www.quizony.com/what-emotion-are-you-feeling-right-now/"+str(i)+".html"
		q = scrape_display(url)
		question_list.append(q)

	#print(question_list)
	

	return route_question(question_list[:4])


@app.route('/get_depr_results', methods=["GET","POST"])
def get_depr_results():
	answers = request.args.get('array')
	return route_depr_results(answers)


if (__name__ == "__main__"):
    app.run(debug=True)