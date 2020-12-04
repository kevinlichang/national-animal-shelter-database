from flask import Flask, render_template, url_for, request, redirect
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
    query = "SELECT animal_id, name, type, shelter_name, shelters.address_city, shelters.address_state FROM `animals` INNER JOIN `shelters` ON animals.location_shelter = shelters.shelter_id;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('animals.html', title='Animals', allAnimals=result)

@app.route("/animals/", methods=["POST"])
def addNewAnimal():
    DBConnect = connectDB()

    animalName = request.form['animalName']
    animalType = request.form['animalType'] 
    animalShelterID = request.form['animalShelterID']
    animalCageID = request.form['animalCageID']
    animalSex = request.form['animalSex']
    animalAdopted = request.form.get('animalAdopted')
    if animalAdopted != "1":
        animalAdopted = "0"

    animalWeight = request.form['animalWeight']

    animalFosterID = request.form['animalFosterID']
    if animalFosterID == "":
        animalFosterID = None

    if animalFosterID == None:
        animalFostered = "0"
    else:
        animalFostered = "1"

    animalChipID = request.form['animalChipID']
    if animalChipID == "":
        animalChipID = None

    animalDescription = request.form['animalDescription']
    if animalDescription == "":
        animalDescription = None
    
    if animalAdopted == "1":
        availableForAdoption = "0"
    else:
        availableForAdoption = "1"

    print(animalChipID)
    print(animalFosterID)
    print(animalDescription)
    
    query = "INSERT INTO `animals`(`name`, `location_shelter`, `location_cage`, `chip_id`, `type`, `sex`, `weight_in_pounds`, `description`, `adopted`, `fostered`, `foster_parent`, `available for adoption`) VALUES (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)"
    data = (animalName, animalShelterID, animalCageID, animalChipID, animalType, animalSex, animalWeight, animalDescription, animalAdopted, animalFostered, animalFosterID, availableForAdoption)
    executeQuery(DBConnect, query, data)
    return redirect('/animals/')

@app.route('/animalProfile/<int:animalId>')
def animalProfile(animalId):
    DBConnect = connectDB()
    query = "SELECT animal_id, name, shelter_name, cage_name, chip_id, type, sex, weight_in_pounds, description, fostered, `available for adoption`, foster_parent FROM animals INNER JOIN shelters ON animals.location_shelter = shelters.shelter_id INNER JOIN cages ON animals.location_cage = cages.cage_id WHERE animal_id = %s;"
    data = str(animalId)
    data = (data,)
    resultAll = executeQuery(DBConnect, query, data).fetchall()
    fosterResult = (0,0)

    if resultAll[0][9] == 1:
        query = "SELECT first_name, last_name FROM `fosters` WHERE foster_id = %s;"
        fosterData = str(resultAll[0][11])
        fosterData = (fosterData,)
        fosterResult = executeQuery(DBConnect, query, fosterData).fetchall()
        

    query = "SELECT first_name, last_name FROM animals_trainers INNER JOIN trainers ON animals_trainers.trainer_id = trainers.trainer_id WHERE animals_trainers.animal_id = %s;"
    resultTrainer = executeQuery(DBConnect, query, data).fetchall()

    return render_template('animalProfile.html', title='Animals Profile', animal=resultAll[0], foster=fosterResult[0], trainerList=resultTrainer)

@app.route("/cages/")
def cages():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT cage_id, shelter_name, cage_location, cage_name, animal_type, capacity FROM `cages` INNER JOIN `shelters` ON cages.shelter_id = shelters.shelter_id;"
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