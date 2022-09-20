# necessary imports
from fileinput import filename
from flask import Flask, request, render_template, redirect
from forms import ContactForm
from flask_mail import Message, Mail
import pandas as pd
import os

mail = Mail()
app = Flask(__name__, static_folder='static')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'chrisostomaki.eva@gmail.com'
#app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
mail.init_app(app)

def find_movie(file, movies):
    groupRec = {}
    rec = {}
    iter = 0
    count = 0
    change_rec = -1

    with open(file+".txt") as f:
        for l in f:
            if "Iteration" in l:
                groupRec = {}
                count = 0
                change_rec+=1
                continue
            count = count + 1

            rec = {}
            firstSplit = l.split("[")
            id = firstSplit[0]
            allRecs = firstSplit[1].replace("]","")
            
            allRecs = allRecs.replace("\n","")
            
            secondSplit = allRecs.split(",")
            
            for r in secondSplit:
                itm = r.split(":")
                rec[itm[0]] = itm[1]
            
            if count <= 5:
                groupRec[id] = rec
                if groupRec[id].get(movies[change_rec]) == None:
                    print("Not Present")
                    
                else:
                    print(groupRec[id][movies[change_rec]])
                
                print(movies[change_rec])
                iter = iter + 1
                
    return groupRec[id]

# index page
@app.route('/')
@app.route('/index')
def index():

    # arrays to store each score
    ov_sat = []
    max_min = []
    ndcg = []
    dfh = []
    f_score = []
    test = []

    with open('MovieLens_AllScores.txt') as all_scores:
        count = 1
        for line in all_scores:
            if count <= 16:
                ov_sat.append(line)
            elif count >= 18 and count <= 33:
                max_min.append(line)
            elif count >= 35 and count <= 50:
                ndcg.append(line)
            elif count >= 52 and count <= 67:
                dfh.append(line)
            elif count >= 69:
                f_score.append(line)

            count += 1

    with open('4_1GroupsTest.txt') as test_file:
        for line in test_file:
            test.append(line.split()[0])


    

    recs = open("Recommended_Movies.txt",'r').read().splitlines() 

    find_movie("4_1/"+test[0], recs)
 


    return render_template('index.html', used_file="MovieLens_AllScores",
                           ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score,
                           recs=recs, test=test[0])

# about page
@app.route('/about')
def about():
    return render_template('about.html')

# contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        msg = Message(request.form.get('subject'), sender=request.form.get('email'),
                      recipients=['chrisostomaki.eva@gmail.com'],
                      body=request.form.get('message')
                      )
        mail.send(msg)
        return 'Form sent.'
    elif request.method == 'GET':
        return render_template('contact.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
