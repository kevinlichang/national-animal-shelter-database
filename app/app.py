from flask import Flask, render_template, url_for, request
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

@app.route("/shelters/", methods=["POST", "GET"])
def addNewShelter():
    DBConnect = connectDB()

    # data taken from addShelterForm
    shelterName = request.form['shelterName']
    shelterAddress = request.form['shelterAddress']
    shelterCity = request.form['shelterCity']
    shelterState = request.form['shelterState']
    shelterZip = request.form['shelterZip']
    shelterAnimalQuantity = request.form['shelterAnimalQuantity']
    shelterCageQuantity = request.form['shelterCageQuantity']
    shelterTotalCageCapacity = request.form['shelterTotalCageCapacity']
    shelterCurrAmtFosterParents = request.form['shelterCurrAmtFosterParents']
    shelterCurrAmtAnimalsFostered = request.form['shelterCurrAmtAnimalsFostered']
    shelterRescureGrp = request.form.get('shelterRescureGrp')
    if shelterRescureGrp != "1":
        shelterRescureGrp = "0"
    print(shelterRescureGrp)


    # INSERT Query
    query = "INSERT INTO `shelters` (`shelter_name`, `address_street`, `address_city`, `address_state`, `address_zip`, `animal_quantity`, `cage_quantity`, `total_cage_capacity`, `current_amt_foster_parents`, `current_amt_animals_fostered`, `rescue_group`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (shelterName, shelterAddress, shelterCity, shelterState, shelterZip, shelterAnimalQuantity, shelterCageQuantity, shelterTotalCageCapacity, shelterCurrAmtFosterParents, shelterCurrAmtAnimalsFostered, shelterRescureGrp)
    executeQuery(DBConnect, query, data)
    return shelters()

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

@app.route("/cages/", methods=["POST", "GET"])
def addNewCage():
    DBConnect = connectDB()

    # data taken from addCageForm
    cageShelterID = request.form['cageShelterID']
    cageLocation = request.form['cageLocation']
    cageName = request.form['cageName']
    cageAnimalType = request.form['cageAnimalType']
    cageCapacity = request.form['cageCapacity']

    # INSERT Query
    query = "INSERT INTO `cages` (`shelter_id`, `cage_location`, `cage_name`, `animal_type`, `capacity`) VALUES (%s,%s,%s,%s,%s)"
    data = (cageShelterID, cageLocation, cageName, cageAnimalType, cageCapacity)
    executeQuery(DBConnect, query, data)
    return redirect("/cages/")

@app.route("/cages/update/<int:id>", methods=["POST"])
def updateCage(id):
    DBConnect = connectDB()

    
    cageShelterID = request.form['cageShelterID']
    cageLocation = request.form['cageLocation']
    cageName = request.form['cageName']
    cageAnimalType = request.form['cageAnimalType']
    cageCapacity = request.form['cageCapacity']

    print(request.form)

    query = "UPDATE cages SET shelter_id = %s, cage_location = %s, cage_name = %s, animal_type = %s, capacity = %s WHERE cage_id = %s"
    data = (cageShelterID, cageLocation, cageName, cageAnimalType, cageCapacity, id)
    result = executeQuery(DBConnect, query, data)
    return redirect("/cages/")

@app.route("/cages/delete/<int:id>", methods=["POST"])
def deleteCage(id):
    DBConnect = connectDB()

    query = "DELETE FROM cages WHERE cage_id = %s"
    data = (id,)
    result = executeQuery(DBConnect, query, data)
    return redirect("/cages/")


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