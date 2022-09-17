# necessary imports
from fileinput import filename
from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__, static_folder='static')

# index page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    
    # arrays to store each score
    ov_sat = []
    max_min = []
    ndcg = []
    dfh = []
    f_score = []


    with open('AllGroups_Goodreads_FScore.txt') as my_file:
        count = 0;
        for line in my_file:
            if count<=15:
                ov_sat.append(line)
            elif count>=16 and count<=31:
                max_min.append(line)
            elif count>=32 and count<=47:
                ndcg.append(line)
            elif count>=48 and count<=63:
                dfh.append(line)
            elif count>=64:
                f_score.append(line)
            
            count+=1;


    return render_template('index.html', value="AllGroups_Goodreads_FScore",
                           ov_sat=ov_sat, max_min=max_min, ndcg=ndcg, dfh=dfh, f_score=f_score)

# about page
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
