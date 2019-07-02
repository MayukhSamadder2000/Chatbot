from flask import Flask, request, jsonify, render_template
import os
import requests
import json
import random
import spacy
random.choice([1, 2, 3])
nlp = spacy.load('en_core_web_sm')
from textblob.classifiers import NaiveBayesClassifier as NBC
#project_root = os.path.dirname(os.path.realpath(os.path.join(__file__, '..', '..')))
misswords=["Sorry I didn't get you","I apologize i couldnt decifer you","Sorry i am Dumb","Can you repeat it please?"
           ,"Pardon?","I am not a human so Plz cooporate sir","I didn't get you"]
with open('C:\\Users\\Mayukh\\Desktop\\ChatBOT\\ChatTemplate\\file.json','r') as json2:
    data=json.load(json2)
training=[]
for i in data:
    for sentence in data[i]['train']:
        training.append((sentence,i))
model=NBC(training)
app = Flask(__name__,
            static_url_path='',
            static_folder='static')

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/chat')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    chat = request.form['message']
    print(chat)
    return jsonify({ "message":returnDialouge(data,intentcheck(chat),entities(chat))})


def intentcheck(string):
    return model.classify(string)
def entities(string):
    doc=nlp(string)
    li=[]
    for entity in doc.ents:
        li.append({entity.label_:entity.text})
    return li

def returnDialouge(data,intent,entity):
    if intent=='useless':
        return random.choice(misswords)
    elif intent in data.keys():
        enk=[]
        for i in range(len(entity)):
            enk.append(*entity[i].values())
        p=data[intent]['entities']
        print(enk)
        if len(p)!=0:
            for value in enk:
                k = 0
                while k<len(p):
                    if value in p[k].values():
                        return data[intent]['reply'][k]
                    k += 1
        else:
            return random.choice(data[intent]['reply'])

    else:
        return random.choice(misswords)


chat = "Tuesday will be fine"
print("Intent:",intentcheck(chat))
print("Entities:",entities(chat))
print("Dialog:",returnDialouge(data,intentcheck(chat),entities(chat)))

# run Flask app
if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=5000 )