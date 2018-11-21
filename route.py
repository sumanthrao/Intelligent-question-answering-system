
from flask import render_template, redirect, url_for, request, session, flash
import indicoio
indicoio.config.api_key = '72571b31b550e2f29f0ed2014ee5d968'


def route_index():
    return render_template("index.html")

def route_result():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        color=request.form['color']
        #thoughts=request.form['thoughts']
        output=[]
        output.append(name)
        output.append(email)
        output.append(color)
        # single example
        indicoio.emotion("I love writing code!")

# batch example
        result=indicoio.emotion(output)
        emotions=[]
        surprise=0
        sadness=0
        joy=0
        fear=0
        anger=0
        combined_emotion=[]
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
