
from flask import render_template, redirect, url_for, request, session, flash
import json
import indicoio
indicoio.config.api_key = '72571b31b550e2f29f0ed2014ee5d968'


def route_index():
    return render_template("index.html")

def route_result():
    if request.method == 'POST':
        
        thoughts = request.form['mythoughts']
        
        #day = request.form['day']
        
        
        output=[]
        
        output.append(thoughts)
        # output.append(day)
        
        results = indicoio.emotion(output)

        print("results: ", results)

        emotions = {
            "surprise": 0,
            "sadness": 0,
            "joy": 0,
            "fear": 0,
            "anger": 0
        }
        
        for result in results:
            for emotion in result:
                emotions[emotion] += result[emotion]

         
        for emotion in emotions:
            emotions[emotion] /= len(output)
        
        print("emotions: ", emotions)
        
        dominant_emotion = max(emotions, key = lambda x: emotions[x])

        print("dominant_emotion", dominant_emotion)

        ret = {
            "fear": {
                "title": "Why this fear?!",
                "quote": "You gain strength, courage, and confidence by every experience in which you really stop to look fear in the face. You are able to say to yourself, 'I lived through this horror. I can take the next thing that comes along.'"
            },
            "joy": {
                "title": "Someone here is happy!! :)",
                "quote": "Happiness is the secret to all beauties....There is no beauty without happiness"
            },
            "surprise": {
                "title": "Woah you seem to be surprised xD",
                "quote": "When I was born I was surprised.....I didnt talk for for a year and a half!!!!"
            },
            "sadness": {
                "title": "I am sad too :(",
                "quote": "This might be a sad chapter but you ARENT a sad story!"
            },
            "anger": {
                "title": "Don\'t angry me he said and look what they did!! xD",
                "quote": "Anger is one letter short of Danger!! Dont Let anger overpower you"
            }
        }

        #output.append(thoughts)

    return render_template("result_pre.html", image="/static/img/" + dominant_emotion + ".jpg", emotion=[emotions], data = ret[dominant_emotion])

def route_question(questions):
    return render_template("qa.html",questions = questions)

def route_depr_results(answers):

    d = json.loads(answers)
    
    # batch example
    output = []
    for str in d:
        output.append(str.split(":")[-1])
    print(output)
    result = indicoio.emotion(output)
    emotions = []
    surprise = 0
    sadness = 0
    joy = 0
    fear = 0
    anger = 0
    combined_emotion = []
    for i in result:
        happy=i['surprise']+i['joy']
        sad=i['fear']+i['anger']+i['sadness']
        surprise=i['surprise']+surprise
        sadness=i['sadness']+sadness
        joy=i['joy']+joy
        fear=i['fear']+fear
        anger=i['anger']+anger
        
        emotions.append({'happy':happy,"sad":sad})
    print(emotions)
    combined_emotion.append({'joy':joy/len(result),'sadness':sadness/len(result),'fear':fear/len(result),'anger':anger/len(result),'surprise':surprise/len(result)})

    happy=0
    sad=0
    verdict={}
    for i in emotions:
        happy=i['happy']+happy
        sad=i['sad']+sad
    verdict['happy']=happy/len(emotions)
    verdict['sad']=sad/len(emotions)

    print(verdict)
    print(combined_emotion)
    



    #output.append(thoughts)

    return render_template("result.html",output=verdict,emotion=combined_emotion)
