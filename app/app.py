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
                    #print("Not Present")

                else:
                    # print(groupRec[id][movies[iter]])
                    mov_scores.append(groupRec[id][movies[iter]])

    return mov_scores

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

    # read groups for testing
    test = open("4_1GroupsTest.txt", 'r').read().splitlines()

    # read recommended movies for these groups
    recs = open("Recommended_Movies.txt", 'r').read().splitlines()

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

    # send results based on button clicked
    if request.method == 'POST':
        # iterate through every test file
        for i in range(0, len(test)):
            # check if that file is the one selected on the table
            if request.form.get(test[i].split("\t", 1)[0]) == test[i].split("\t", 1)[0]:
                # create new list with the movie recommendations and individual scores
                # of that specific group
                new_list = list(
                    filter(lambda id: id.get('id') ==
                           test[i].split("\t", 1)[0], items)
                )
                return render_template('index.html', items=new_list, used_file="MovieLens_AllScores",
                                       ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score,
                                       test=test, test_file="Recommended_Movies")

    return render_template('index.html', used_file="MovieLens_AllScores",
                           ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score,
                           test=test, test_file="Recommended_Movies")

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


@app.route("/yourform/getinfo")
def show_sorted_info():
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)
