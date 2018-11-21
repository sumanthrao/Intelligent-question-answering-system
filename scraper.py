from bs4 import BeautifulSoup

import requests



def scrape_display(url):
    # outputs a dictionary 	
    r  = requests.get(url)
    question  = []
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    for p in soup.findAll('p', {'class': 'text-primary textOfQuestion'}):   
        question.append(p.text.strip())
    for b in soup.findAll('div',{'class':'btn-group-vertical btn-group btn-group-lg'}): 
        for btn in b.findAll('button'): 
            question.append(btn.text.strip()) 
    return question 
            

question_list = []

for i in range(1,29):
    
    url = "https://www.quizony.com/what-emotion-are-you-feeling-right-now/"+str(i)+".html"
    q = scrape_display(url)
    question_list.append(q)
    

print(question_list)

