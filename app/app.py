# necessary imports
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from forms import ContactForm
from flask_mail import Message, Mail
import pandas as pd
import os

mail = Mail()
app = Flask(__name__, static_folder='static')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.name}>'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'chrisostomaki.eva@gmail.com'
#app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
mail.init_app(app)

# function to find the score given by each member to the
# recommended movies in the file


def find_movie(file, movies):
    groupRec = {}
    rec = {}
    iter = -1
    count = 0
    mov_scores = []

    with open(file+".txt") as f:
        for l in f:
            if "Iteration" in l:
                groupRec = {}
                count = 0
                iter += 1
                continue

            count = count + 1

            rec = {}
            firstSplit = l.split("[")
            id = firstSplit[0]
            allRecs = firstSplit[1].replace("]", "")

            allRecs = allRecs.replace("\n", "")

            secondSplit = allRecs.split(",")

            for r in secondSplit:
                itm = r.split(":")
                rec[itm[0]] = itm[1]

            if count <= 5:
                groupRec[id] = rec
                if groupRec[id].get(movies[iter]) == None:
                    mov_scores.append("Not Present")

                else:
                    mov_scores.append(groupRec[id][movies[iter]])

    return mov_scores

# function to get individual scores
# and create a dictionary to store them


def individual_scores(test, recs):
    mov_scores = {}
    items = []

    t = 0  # index for group file
    m = 0  # index for recommended movie
    start = 0  # starting index for recommended movies
    end = 15  # final index for recommended movies

    for t in range(0, len(test)):

        # find invividual scores for the recommended movies
        mov_scores = find_movie(
            "4_1/"+test[t].split("\t", 1)[0], recs[start:end])

        # create a dictionary to store invividual scores and recommended movies
        s = 0
        for i in range(0, 15):
            i = str(i)

            an_item = dict(id=test[t].split("\t", 1)[0], movie=recs[m], round=i, m1_score=mov_scores[s], m2_score=mov_scores[s+1],
                           m3_score=mov_scores[s+2], m4_score=mov_scores[s+3], m5_score=mov_scores[s+4])
            items.append(an_item)

            s += 5
            m += 1

        t += 1
        start += 15
        end += 15

    return items


# function to find the score given by each member to the
# movie that was not recommended

def find_why_not_movie(file, movie_id, round):
    groupRec = {}
    rec = {}
    count = 0
    mov_scores = []
    iter = 0

    with open(file+".txt") as f:
        for l in f:
            if "Iteration " + round in l:
                iter = 1
                continue
            elif "Iteration " + str(int(round)+1) in l:
                break
            elif "Iteration" in l:
                continue

            if iter == 1:
                count = count + 1

                rec = {}
                firstSplit = l.split("[")
                id = firstSplit[0]
                allRecs = firstSplit[1].replace("]", "")

                allRecs = allRecs.replace("\n", "")

                secondSplit = allRecs.split(",")

                for r in secondSplit:
                    itm = r.split(":")
                    rec[itm[0]] = itm[1]

                if count <= 5:
                    groupRec[id] = rec
                    if groupRec[id].get(movie_id) == None:
                        mov_scores.append("Not Present")

                    else:
                        mov_scores.append(groupRec[id][movie_id])

    return mov_scores


# function to get individual scores
# for movie that was not recommended

def why_not_movie(group, movie_id, round_id):
    mov_scores = find_why_not_movie(
            "4_1/"+group, movie_id, round_id)

    return mov_scores

# read dictionary from file


def parse(d):
    dictionary = dict()
    pairs = d.strip('{}').split(', ')
    for i in pairs:
        pair = i.split(': ')
        dictionary[pair[0].strip('\'\'\"\"')] = pair[1].strip('\'\'\"\"')
    return dictionary

# index page


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    # arrays to store each score
    ov_sat = []
    max_min = []
    ndcg = []
    dfh = []
    f_score = []

    with open('files/MovieLens_AllScores.txt') as all_scores:
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

    # read groups for testing
    test = open("files/4_1GroupsTest.txt", 'r').read().splitlines()

    # read recommended movies for these groups
    recs = open("files/Recommended_Movies.txt", 'r').read().splitlines()

    # get individual scores
    items = individual_scores(test, recs)

    # send results based on button clicked
    if request.method == 'POST':
        # iterate through every test file
        for i in range(0, len(test)):
            # check if that file is the one selected on the table
            if request.form.get(test[i].split("\t", 1)[0]) == test[i].split("\t", 1)[0]:
                # create new list with the movie recommendations and individual scores
                # of that specific group
                recs_scores = list(
                    filter(lambda id: id.get('id') ==
                           test[i].split("\t", 1)[0], items)
                )

                return render_template('index.html', items=recs_scores,
                                       ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score)
    
    return render_template('index.html',test=test,
                           ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score)


# watch_next page


@app.route('/watch_next', methods=['GET', 'POST'])
def watch_next():
    # read groups for testing
    test = open("files/4_1GroupsTest.txt", 'r').read().splitlines()

    # read recommended movies for these groups
    recs = open("files/Recommended_Movies.txt", 'r').read().splitlines()

    # get individual scores
    items = individual_scores(test, recs)

    # file to save current round of each group
    open("files/Current_Round.txt", "a")

    # get scores per round
    iter_scores = open('files/Scores_Per_Round.txt', 'rt')
    score_lines = iter_scores.read().split('\n')

    # send results based on button clicked
    if request.method == 'POST':
        
        # arrays to store each score
        ov_sat = []
        max_min = []
        ndcg = []
        dfh = []
        f_score = []
        cur_round = []

        movie_id = request.form.get('movie_id')

        # check if why not query was requested
        if(movie_id != None):
            group = request.form.get("group_id")
            round = request.form.get("round_id")
            movie_scores = why_not_movie(group, movie_id, round)
            return render_template('watch_next.html', group = group, movie_id = movie_id, movie_scores = list(movie_scores))

        for i in range(0, len(test)):
            group = request.form.get(test[i].split("\t", 1)[0])
            # check if that file is the one which button was pressed
            if group == test[i].split("\t", 1)[0]:

                # create new list with the movie recommendations and individual scores
                # of that specific group
                recs_scores = list(
                    filter(lambda id: id.get('id') ==
                           test[i].split("\t", 1)[0], items)
                )                
                    
                # read file to get the current round
                with open('files/Current_Round.txt', 'r') as fp:
                    lines = fp.readlines()
                    for line in lines:
                        if line.find(str(group)) != -1:
                            round = (line[-3:-1])

                if int(round) != 15:                      
                    # replace previous round with current round
                    with open('files/Current_Round.txt', 'r') as file :
                        filedata = file.read()

                    filedata = filedata.replace(str(group) + " " + str(round), str(group) + " " + str("{0:0=2d}".format(int(round)+1)))

                    with open('files/Current_Round.txt', 'w') as file:
                        file.write(filedata)

                    # store all the previous scores
                    previous_scores = []
                    
                    for entry in recs_scores:
                        if(int(entry['round'])<= int(round)-1):
                            previous_scores.append(entry)

                    # show only the recommendation of the current round
                    cur_round_scores = list(
                                filter(lambda index: index.get('round') == str("{0:0=1d}".format(int(round))), recs_scores)
                            )

                    # get scores for each round of that specific group
                    for l in score_lines:
                        if l != '':
                            dictionary = parse(l)
                            if(dictionary['group'] == group):
                                if(int(dictionary['round']) == int(round)):
                                    cur_round.extend((dictionary['ov_sat'],dictionary['max_min'],dictionary['ndcg'],dictionary['dfh'],dictionary['f_score']))
                                elif(int(dictionary['round']) <= int(round)-1):
                                    ov_sat.append(dictionary['ov_sat'])
                                    max_min.append(dictionary['max_min'])
                                    ndcg.append(dictionary['ndcg'])
                                    dfh.append(dictionary['dfh'])
                                    f_score.append(dictionary['f_score'])
                                

                    return render_template('watch_next.html', items=cur_round_scores, previous_scores=previous_scores,
                                            ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score, cur_round = cur_round)

                # show all recommendations
                elif int(round) == 15:

                    # get scores for every round of that specific group
                    for l in score_lines:
                        if l != '':
                            dictionary = parse(l)
                            if(dictionary['group'] == group):
                                ov_sat.append(dictionary['ov_sat'])
                                max_min.append(dictionary['max_min'])
                                ndcg.append(dictionary['ndcg'])
                                dfh.append(dictionary['dfh'])
                                f_score.append(dictionary['f_score'])

                    return render_template('watch_next.html', previous_scores=recs_scores, 
                                            message="Maximum number of rounds has been reached. See all previous rounds here: ",
                                            ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score)



    iter_scores.close()
    name = request.args['name']  # counterpart for url_for()
    name = session['name']  
    return render_template('watch_next.html', test=test, user = name)

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

# login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username'], password=request.form['password']).first()
        if user!= None:
            name = user.name
            session['name'] = name
            return redirect(url_for('watch_next', name = name))
        else:
             error = 'Invalid Credentials. Please try again.'
            
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)
