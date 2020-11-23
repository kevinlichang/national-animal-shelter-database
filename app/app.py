from flask import Flask, render_template, url_for
from backend.dbConnector import connectDB, executeQuery

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/shelters/")
def shelters():
    return render_template('shelters.html', title='Shelters')

@app.route("/animals/")
def animals():
    return render_template('animals.html', title='Animals')

@app.route("/cages/")
def cages():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT * from cages;"
    result = executeQuery(DBConnect, query)
    result.fetchone()
    print(result)
    return render_template('cages.html', title='Cages', allCages=result)

@app.route("/fosters/")
def fosters():
    return render_template('fosters.html', title='Fosters')

@app.route("/trainers/")
def trainers():
    return render_template('trainers.html', title='Trainers')

if __name__ == '__main__':
    app.run(debug=True)