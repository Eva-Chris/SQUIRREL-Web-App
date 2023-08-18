# SQUIRREL Movies Web App

The source code for the paper:

Eva Chrysostomaki, Maria Stratigi, Vasilis Efthymiou, Kostas Stefanidis and Dimitris Plexousakis. Fair Sequential Group Recommendations in SQUIRREL Movies (poster). [Tabular Data Analysis Workshop (TaDA)@VLDB 2023](https://tabular-data-analysis.github.io/tada2023/) [[pdf](https://drive.google.com/file/d/1M0sHJ6vjq6nPHWG8nQlOMZLrDtH0A_Ls/view)]

which is part of the project <a href="https://isl.ics.forth.gr/ResponsibleER/">ResponsibleER: Responsible by Design Entity Resolution</a>, 
funded by the <a href="https://www.elidek.gr/en/homepage/">Hellenic Foundation for Research and Innovation</a>.


/app  <br>
&emsp;&emsp;   /static <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /css/style.css --- The css file with the page styling <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /images --- The images used in the app <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /js/highchartTable.js --- JS file containing the code for the Highchart Table plugin <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /paper --- The SQUIRREL paper <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /posters --- Posters for the recommended movies <br>
&emsp;&emsp;   /templates <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /about.html --- Abstract from SQUIRREL paper and link to full paper <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /contact.html --- Page with contributors' contact information <br>
&emsp;&emsp;&emsp;&emsp;&emsp;   /watch_next.html --- Group selection to view movie recommendations <br>
&emsp;&emsp;   /app.py --- Main python file <br>
/files   
&emsp;&emsp; /Current_Round.txt --- Saves current round for each group <br>
&emsp;&emsp; /Recommended_Movies_Average.txt --- Reccomended movie and actions for each group using Average method <br>
&emsp;&emsp; /Recommended_Movies_Fscore.txt --- Reccomended movie and actions for each group using FScore method <br>
&emsp;&emsp; /Scores_Per_Round_Average.txt --- All scores for each group using Average method <br>
&emsp;&emsp; /Scores_Per_Round_Fscore.txt --- All scoresfor each group using Fscore method <br>
/requirements.py --- Python script to install the required libraries <br>

---ACTIVATING VIRTUAL ENVIRONMENT--- <br>
If env folder is not available type: python3 -m venv env

To activate the virtual environment type: source env/bin/activate

If flask is not installed type: pip install flask

---CHANGING ENVIRONMENT---<br>
In Visual Studio Code press Ctrl+Shift+P and select venv as Python Intepreter

---OPENING THE WEBSITE---<br>
Type: python3 app/app.py

The server starts on: http://127.0.0.1:5000 or localhost:5000
