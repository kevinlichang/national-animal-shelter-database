from flask import Flask, render_template, url_for
from backend.dbConnector import connectDB, executeQuery

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/shelters/")
def shelters():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT * from shelters;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('shelters.html', title='Shelters', allShelters=result)

@app.route("/animals/")
def animals():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT * from animals;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('animals.html', title='Animals', allAnimals=result)

@app.route("/cages/")
def cages():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT * from cages;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('cages.html', title='Cages', allCages=result)

@app.route("/fosters/")
def fosters():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT * from fosters;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('fosters.html', title='Fosters', allFosters=result)

@app.route("/trainers/")
def trainers():
    return render_template('trainers.html', title='Trainers')

if __name__ == '__main__':
    app.run(debug=True)