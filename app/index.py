from flask import Flask, request, jsonify, render_template,url_for, flash, redirect,session
import os
import dialogflow
import requests
import json
import pusher
from pymongo import MongoClient
import json, pprint
from forms import RegistrationForm, LoginForm
from bs4 import BeautifulSoup
import googletrans
import langdetect
import spacy
from spacy_cld import LanguageDetector
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)


client = MongoClient('localhost', 27017)
description_list=[]
link_list=[]
document_list=[]
title_list=[]
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
logged_in=0
lang_flag = 0

print(os.getenv('PUSHER_APP_ID'))
# initialize Pusher
pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True)

db = client.gov_data
db_users = client.user_data
result1= db.policies.find({})
result2=list(db.policies.find({}))
db = client.chatbot_search
result3 = list(db.policies.find({}))

# Spacy things
nlp = spacy.load('en')
language_detector = LanguageDetector()
nlp.add_pipe(language_detector)

#print(result2[:2])
number=0
found_user = []

@app.route("/", methods=['GET', 'POST'])
def policies():
    return render_template('policies.html', policies = result2)



@app.route('/index')
def index():
    if(logged_in==0):
        return redirect(url_for('login'))
    else:
        return render_template('index.html', policies = result2, users = found_user)


@app.route('/layout')
def layout():
    return render_template('layout.html', policies=result2 , users=found_user)

@app.route('/my_webhook/', methods=['POST'])
def get_policy_detail():
    global lang_flag
    # doc = nlp('This is some English text.')
    response=''
    trans = googletrans.Translator()
    a = request.get_json(silent=True)
    print(a)
    if (a["queryResult"]["queryText"].isnumeric()):
        lang_flag = 0
        print('yep')  
        #print(lang._.language_scores['en'])
    
    translated = trans.translate(a["queryResult"]["queryText"] ,src='hi', dest='en')
    print(translated.text)

    
    if "isFallback" in a['queryResult']["intent"]:
        # print('Siiiiiiiiiiiiiiii')
        if a['queryResult']["intent"]["isFallback"]==True:
            print('yep')
            myText= a['queryResult']['queryText']
            index=0
            j=1
            flag=0
            
            print(myText)
            for i in result2:
                index+=1
                # print('title' in i.keys(), 'Title' in i.keys())
                
                if(myText.lower() in i['Title'].lower()):
                    # print(i['Title'])
                    if lang_flag==0:
                        response+="<div class='btn btn-primary btn-modal btn"+str(index)+"' onclick='openModal(this)' data-toggle='modal' style='max-width:20em; border-radius:20px; white-space:initial;height:62px;'> "+str(j)+" : "+i['Title']+'</div>'
                    else:
                        response+="<div class='btn btn-primary btn-modal btn"+str(index)+"' onclick='openModal(this)' data-toggle='modal' style='max-width:20em; border-radius:20px; white-space:initial;height:62px;'> "+str(j)+" : "+trans.translate(i['Title'],src="en",dest="hi").text+'</div>'
                    j+=1
                    print(response)
                    flag=1
        response+= a['queryResult']['fulfillmentText']
    else:
        k=1
        l=1
        n=1
        m=1
        flag=0
        print("yepeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

        if 'Policy' in a['queryResult']['parameters']:
            description_list.clear()
            link_list.clear()
            document_list.clear()
            title_list.clear()
            if lang_flag !=1:
                response+=a['queryResult']['fulfillmentText']
                print("in english", lang_flag)
            else:
                response+=trans.translate(a['queryResult']['fulfillmentText'], src='en', dest='hi').text
                print("in hindi", lang_flag)
            # print('aa',response)

            for i in range(0, 20):
                try:
                    if(a['queryResult']['parameters']['Policy'][0].lower() in [i.lower() for i in result1[i]['keywords']]):
                        id = str(i+1)
                        #print(id)
                        if lang_flag != 1:
                            response+="<br>"+"<div class='btn btn-primary btn-modal btn"+id+"' onclick='openModal(this)' data-toggle='modal' style='max-width:20em; border-radius:20px; white-space:initial;height:62px;'>"+ str(k) +": "+(result1[i]["Title"])+'</div>' 
                            
                        else:
                            response+="<br>"+"<div class='btn btn-primary btn-modal btn"+id+"' onclick='openModal(this)' data-toggle='modal' style='max-width:20em; border-radius:20px; white-space:initial;height:62px;'>"+ str(k) +": "+trans.translate((result1[i]["Title"]),src="en",dest="hi").text+'</div>' 
                            
                        title_list.insert(m, result1[i]["Title"])
                        description_list.insert(k, result1[i]["Description"])
                        link_list.insert(n, result1[i]["Links"])
                        document_list.insert(l, result1[i]["docs"])
                    
                        
                        
                        m+=1
                        n+=1
                        k+=1
                        l+=1

                        flag=1
                except:
                    print(a)
            if lang_flag ==0:    
                response+=""+"Enter a number for more details:"  
            else:
                response+=""+trans.translate("Enter a number for more details:",src="en",dest="hi").text


        elif 'number' in a['queryResult']['parameters']:
            global number
            
            number=a['queryResult']['parameters']['number']
            # print(number)
            if 'information' in a['queryResult']['parameters']:
                if a['queryResult']['parameters']['information']!="":
                    if lang_flag==0:
                        response+="<b>Title </b>: "+title_list[int(number-1)]+"<br>"+"<b>Description </b>: "+description_list[int(number-1)]+"<br>"+"<b>Link</b> : "+link_list[int(number-1)]+"<br><b>Documents</b> : "
                    else:
                        response+="<b>Title </b>: "+trans.translate(title_list[int(number-1)],src="en",dest="hi").text+"<br>"+"<b>Description </b>: "+trans.translate(description_list[int(number-1)],src="en",dest="hi").text+"<br>"+"<b>Link</b> : "+trans.translate(link_list[int(number-1)],src="en",dest="hi").text+"<br><b>Documents</b> : "
                        for i in range(0, len(document_list)):
                            if i==(int(number-1)):
                                for j in range(0,len(document_list[i])):
                                    if lang_flag==0:
                                        response+="%"+str(j+1)+" : "+document_list[i][j]
                                    else:
                                        response+="%"+str(j+1)+" : "+trans.translate(document_list[i][j],src="en",dest="hi").text
                else:
                   
                    if lang_flag==0:
                        response+=description_list[int(a['queryResult']['parameters']['number'])-1]
                    else:
                        response+=trans.translate(description_list[int(a['queryResult']['parameters']['number'])-1],src="en",dest="hi").text
            else:
                if lang_flag==0:
                    response+=description_list[int(a['queryResult']['parameters']['number'])-1]
                else:
                    response+=trans.translate(description_list[int(a['queryResult']['parameters']['number'])-1],src="en",dest="hi").text
        
            
        elif 'links' in a['queryResult']['parameters']:
            
            print(a['queryResult']['parameters']['links'])
            
            response+="^"+link_list[int(number-1)]
            

        elif 'documents' in a['queryResult']['parameters']:
            # print(a['queryResult']['parameters']['documents'])
            if lang_flag==0:
                response="The needed documents are:"
            else:
                response=trans.translate("The needed documents are:",src="en",dest="hi").text

            for i in range(0, len(document_list)):
                if i==(int(number-1)):
                    for j in range(0,len(document_list[i])):
                        if lang_flag==0:
                            response+="%"+str(j+1)+" : "+document_list[i][j]
                        else:
                            response+="%"+str(j+1)+" : "+trans.translate(document_list[i][j],src="en",dest="hi").text

        elif 'information' in a['queryResult']['parameters']:
            print("in infoooooooooooooooooo")
            if lang_flag==0:
            
                response+="<b>Title </b>: "+title_list[int(number-1)]+"<br>"+"<b>Description </b>: "+description_list[int(number-1)]+"<br>"+"<b>Link</b> : "+link_list[int(number-1)]+"<br><b>Documents</b> : "
                print(response)
                for i in range(0, len(document_list)):
                    if i==(int(number-1)):
                        for j in range(0,len(document_list[i])):
                            response+="%"+str(j+1)+" : "+document_list[i][j]
            else:
                response+="<b>Title </b>: "+trans.translate(title_list[int(number-1)],src="en",dest="hi").text+"<br>"+"<b>Description </b>: "+trans.translate(description_list[int(number-1)],src="en",dest="hi").text+"<br>"+"<b>Link</b> : "+ link_list[int(number-1)]+"<br><b>Documents</b> : "
                print(response)
                for i in range(0, len(document_list)):
                    if i==(int(number-1)):
                        for j in range(0,len(document_list[i])):
                            response+="%"+str(j+1)+" : "+trans.translate(document_list[i][j],src="en",dest="hi").text

    response1 = striphtml(response)

    # print(response)
    reply = {
        "fulfillmentText": response1,
        "fulfillmentMessages": [
      {
        "text": {
          "text": [response]
        }
      }
    ],
    }
    
    return jsonify(reply)

@app.route('/pins')
def pins():
    if(logged_in==0):
        return redirect(url_for('login'))
    else:
        return render_template('pins.html', policies = result2, users=found_user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    form = LoginForm()
  
    if form.validate_on_submit():
        fu = []
        fu = list(db_users.users.find({'emailid': form.email.data, 'pword': form.password.data}))
        if fu:
            global found_user
            
            flash('You have been logged in!', 'success')
            fu = fu[0]
            print(fu)
            fu.pop('_id')
            global logged_in
            
            logged_in=1
            found_user = fu
            return render_template('profile.html',policies = result2,users = found_user)
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route('/send_message', methods=['POST'])
def send_message():
    #socketId = request.form['socketId']
    trans = googletrans.Translator()
    message = request.form['message']
    global lang_flag

    lang = nlp(message)
    print(lang._.languages)

    if 'hi' in lang._.languages or 'bh' in lang._.languages:
        lang_flag = 1
        # print(doc._.language_scores['bh'])
        message = trans.translate(message ,src='hi', dest='en').text
    elif 'en' in lang._.languages or not lang._.languages:
        lang_flag = 0
        print('i am eng')
        
    print(message)
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text, fulfillment_msg = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    
    print(fulfillment_text)
    print(fulfillment_text != "undefined")
    if(fulfillment_text != "undefined"):
        pusher_client.trigger('movie_bot', 'new_message',
                            {'human_message': message, 'bot_message': fulfillment_msg})
                            
    return jsonify(response_text)

@app.route("/register", methods=['GET', 'POST'])
def register():

    flag=0
    form = RegistrationForm()
    if form.validate_on_submit():
    #     if db_users.users.find({'uname': form.username.data}):
    #         flag=1
    #         print("In flag"+str(flag))
        global logged_in
        data={}
        if flag==0:
            
            data={
                "fname":form.firstname.data,
                "mname":form.middlename.data,
                "lname":form.lastname.data,
                "uname":form.username.data,
                "pword":form.password.data,
                "occupation":form.occupation.data,
                "emailid":form.email.data,
                "pinned":[]
            }
           
            db_users.users.insert(data)
            logged_in = 1
            # flash(f'Account created for {form.username.data}!', 'success')
            
        return render_template('index.html',policies = result2, users=data)
        
    else:
        #flash(f'Account not created :(', 'danger')
        return render_template('register.html', title='Register', form=form)



@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if(logged_in==0):
        return redirect(url_for('login'))
    else:
        return render_template('profile.html',policies = result2,users= found_user)

@app.route('/logout')
def logout():
    global logged_in
    session.clear()
    logged_in=0
    return redirect(url_for('login'))

searchpol = []
@app.route('/search', methods = ['GET','POST'])
def searchbar():
    return render_template('search.html', searchpol = searchpol, policies = result2)

@app.route('/polsearch', methods = ['POST'])
def getTemplate():
    searchpol.clear()
    pol = ''
    if request.method == 'POST':
        #print(request.get_json(), request.args.get('a'), request.get_data())
        pol = request.get_data().decode('utf-8')
        #print(pol, 'SMEOTHING JUST LIKE THIS')
        #print('nope')
        pol1 = {}
        if pol:
            pol = pol.replace('+', ' ').split('&') 
            for i in pol:
                pol1[i.split('=')[0]] = i.split('=')[1] 
            for i in result2:
                if(i['Title'].lower() in pol1.values()):
                    #print(i['Title'])
                    #print('start',result2.index(i), 'end')
                    searchpol.append(i)
    #print(searchpol, 'is searchpol')
    soup = BeautifulSoup(render_template('search.html', searchpol = searchpol, policies = result2), 'html.parser')
    tag = soup.find('div', {'id':'card-display'})
    tag = tag.findChildren('div', recursive = False)
    #print(tag)
    return jsonify(cards = str(tag[0]))

@app.route('/addPin', methods = ['POST'])
def pinPol():       
    data = request.get_data().decode('utf-8')
    data = data.replace('+', ' ').split('=')[1]
    for i in result2:
        if data == i['Title']:
            data = i
            print(data.pop('_id', None))
            break
    print(data)
    a = list(db_users.users.find({'uname': found_user['uname']}))[0]
    #print(a)
    a['pinned'].append(data)
    #print(a)
    db_users.users.update({'uname': found_user['uname']}, a)
    found_user['pinned'].append(data)
    return "done"

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

# run Flask app
if __name__ == "__main__":
    app.run()


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        # print(response.query_result, str(response.query_result.fulfillment_messages[0].text)=='', response.query_result.fulfillment_messages[0].text=='')
        if str(response.query_result.fulfillment_messages[0].text)!='':
            return str(response.query_result.fulfillment_messages[0].text.text[0]),response.query_result.fulfillment_text
        else:
            return response.query_result.fulfillment_text, response.query_result.fulfillment_text
