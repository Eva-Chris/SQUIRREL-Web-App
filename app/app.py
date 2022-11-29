# necessary imports
from flask import Flask, request, render_template
from forms import ContactForm
from flask_mail import Message, Mail
import pandas as pd
import os
import json

mail = Mail()
app = Flask(__name__, static_folder='static')
    
# MAIL
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'chrisostomaki.eva@gmail.com'
#app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
mail.init_app(app)

# function to get individual scores
# and create a dictionary to store them


def individual_scores(test, recs):
    mov_scores = {}
    items = []

    t = 0  # index for group file
    
    
    for t in range(0, len(test)):

        # create a dictionary to store invividual scores and recommended movies
        s = 0
        m = 0
        for i in range(0, 15):
            s = 0
            for j in range (0,5):
                i = str(i)
                if m >= len(recs):
                    break
                # find invividual scores for the recommended movies
                mov_scores = find_movie(
                    "4_1/"+test[t].split("\t", 1)[0], recs[m],i)

                an_item = dict(id=test[t].split("\t", 1)[0], movie=recs[m], round=i, m1_score=mov_scores[s], m2_score=mov_scores[s+1],
                            m3_score=mov_scores[s+2], m4_score=mov_scores[s+3], m5_score=mov_scores[s+4])
                items.append(an_item)
                m += 1
        t += 1

    return items


# function to find the score given by each member to the
# recommended movies in the file

def find_movie(file, movie_id, round):
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
                        mov_scores.append("Score < 1")

                    else:
                        mov_scores.append(groupRec[id][movie_id])

    return mov_scores


# function to get individual scores
# for movie that was not recommended

def why_not_movie(group, movie_id, round_id):
    mov_scores = find_movie(
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

# watch_next page


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/watch_next', methods=['GET', 'POST'])
def watch_next():
    
    # read groups for testing
    test = open("files/4_1GroupsTest.txt", 'r').read().splitlines()

    # read recommended movies for these groups
    rec_mov_json = []
    for line in open('files/Recommended_Movies.txt', 'r'):
        rec_mov_json.append(json.loads(line))
    
    recs = []
    for x in rec_mov_json:
        for i in range(0,5):
            recs.append(x['movie'][i]) 

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
            

            recs_scores = list(
                    filter(lambda id: id.get('id') == group, items)   
                ) 
            cur_round_scores = list(
                        filter(lambda index: index.get('round') == str("{0:0=1d}".format(int(round))), recs_scores)
                    )


            return render_template('watch_next.html', movie_id = movie_id, movie_scores = list(movie_scores),cur_not=cur_round_scores)

        for i in range(0, len(test)):
            if(request.form.get("group_id") != None):
                group = request.form.get("group_id")
            else:
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

                    # actions
                    for x in rec_mov_json:
                        if (x['group'] == group):
                            if int(x['round']) ==  int(round):
                                action = int(x['action'])
                    
                    if action == 0:      
                        action = "Average"  
                    elif action == 1:
                        action = "SDAA"
                    elif action == 2:
                        action = "SIAA"
                    elif action == 3:
                        action = "Average Plus"
                    elif action == 4:
                        action = "Pareto"
                    elif action == 5:
                        action = "RP80"
                    else:
                        print("ERROR---ERROR")         
                                

                    return render_template('watch_next.html', items=cur_round_scores, previous_scores=previous_scores,
                                            ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score, cur_round = cur_round, action = action)

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
    return render_template('watch_next.html', test=test)

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
