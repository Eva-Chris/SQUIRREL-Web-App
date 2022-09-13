#necessary imports 
from flask import Flask, request, render_template
from flask_navigation import Navigation
import pandas as pd

app = Flask(__name__,static_folder='static')
nav = Navigation(app)

#navigation bar
nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Extras', 'extras', {'page': 1}),
])

#index page
@app.route('/', methods=['GET', 'POST'])
def index():
    #read every table seperately from file
    ov_sat = pd.read_csv('AllGroups_Goodreads_FScore.txt',nrows=15)
    max_min = pd.read_csv('AllGroups_Goodreads_FScore.txt',skiprows=16,nrows=15)
    ndcg = pd.read_csv('AllGroups_Goodreads_FScore.txt',skiprows=32,nrows=15)
    dfh = pd.read_csv('AllGroups_Goodreads_FScore.txt',skiprows=48,nrows=15)
    f_score = pd.read_csv('AllGroups_Goodreads_FScore.txt',skiprows=64,nrows=15)

    #relevant button displays the results
    if request.method == 'POST':
        if request.form.get('ov_sat') == 'Overall Satisfaction':
            return render_template('index.html', table=[ov_sat.to_html(classes='data')], titles=ov_sat.columns.values)
        elif  request.form.get('max_min') == 'MaxMin':
            return render_template('index.html', table2=[max_min.to_html(classes='data')], titles2=max_min.columns.values)
        elif  request.form.get('ndcg') == 'ndcg':
            return render_template('index.html', table3=[ndcg.to_html(classes='data')], titles3=ndcg.columns.values)
        elif  request.form.get('dfh') == 'dfh':
            return render_template('index.html', table4=[dfh.to_html(classes='data')], titles4=dfh.columns.values)
        elif  request.form.get('f_score') == 'f_score':
            return render_template('index.html', table5=[f_score.to_html(classes='data')], titles5=f_score.columns.values)
        else:
            pass
    elif request.method == 'GET':
        return render_template('index.html')

#extras page
@app.route('/extras/<int:page>')
def extras(page):
    return render_template('extras.html', page=page)

if __name__ == "__main__":
    app.run(debug=True)
