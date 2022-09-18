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
app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
mail.init_app(app)

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

    with open('MovieLens_AllScores.txt') as my_file:
        count = 1;
        for line in my_file:
            if count<=16:
                ov_sat.append(line)
            elif count>=18 and count<=33:
                max_min.append(line)
            elif count>=35 and count<=50:
                ndcg.append(line)
            elif count>=52 and count<=67:
                dfh.append(line)
            elif count>=69:
                f_score.append(line)
            
            count+=1;


    return render_template('index.html', value="MovieLens_AllScores",
                           ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score)

# about page
@app.route('/about')
def about():
    return render_template('about.html')

# contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':        
        msg = Message(request.form.get('subject'), sender = request.form.get('email'),
            recipients = ['chrisostomaki.eva@gmail.com'],
            body= request.form.get('message')
            )  
        mail.send(msg)
        return 'Form sent.'   
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
