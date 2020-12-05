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

    query = "SELECT shelters.shelter_name, shelters.shelter_id FROM shelters ORDER BY shelters.shelter_name;"
    sheltersList = executeQuery(DBConnect, query).fetchall()

    return render_template('animals.html', title='Animals', allAnimals=result, allShelters=sheltersList)

@app.route("/animals/", methods=["POST"])
def addNewAnimal():
    DBConnect = connectDB()

    animalName = request.form['animalName']
    animalType = request.form['animalType'] 
    animalShelterID = request.form['animalShelterID']
    animalSex = request.form['animalSex']
    animalAdopted = request.form.get('animalAdopted')
    if animalAdopted != "1":
        animalAdopted = "0"

    animalWeight = request.form['animalWeight']

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

    query = "INSERT INTO `animals`(`name`, `location_shelter`, `chip_id`, `type`, `sex`, `weight_in_pounds`, `description`, `adopted`, `available for adoption`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (animalName, animalShelterID, animalChipID, animalType, animalSex, animalWeight, animalDescription, animalAdopted, availableForAdoption)
    executeQuery(DBConnect, query, data)
    return redirect('/animals/')

@app.route('/animalProfile/<int:animalId>')
def animalProfile(animalId):
    DBConnect = connectDB()
    query = "SELECT animal_id, name, shelter_name, location_cage, chip_id, type, sex, weight_in_pounds, description, foster_parent, `available for adoption`, animals.location_shelter FROM animals INNER JOIN shelters ON animals.location_shelter = shelters.shelter_id WHERE animal_id = %s;"
    strdata = str(animalId)
    data = (strdata,)
    resultAll = executeQuery(DBConnect, query, data).fetchall()
    fosterResult = (0,0,0)
    fosterList = (None,)
    possible_trainers = (0,0,0)

    query = "SELECT trainers.first_name, trainers.last_name, trainers.trainer_id FROM `shelters_trainers` INNER JOIN `trainers` ON shelters_trainers.trainer_id = trainers.trainer_id INNER JOIN animals_trainers ON trainers.trainer_id = animals_trainers.trainer_id WHERE trainers.animal_specialty = %s AND shelters_trainers.shelter_id = %s AND NOT animals_trainers.animal_id = %s"
    query_AnimalType = str(resultAll[0][5])
    query_ShelterId = str(resultAll[0][11])
    trainData = (query_AnimalType, query_ShelterId, strdata)
    possible_trainers = executeQuery(DBConnect, query, trainData).fetchall()

    if resultAll[0][9] != None:
        query = "SELECT first_name, last_name, foster_id FROM `fosters` WHERE foster_id = %s;"
        fosterData = str(resultAll[0][9])
        fosterData = (fosterData,)
        fosterResult = executeQuery(DBConnect, query, fosterData).fetchall()

    query = "SELECT fosters.first_name, fosters.last_name, fosters.foster_id FROM shelters_fosters INNER JOIN fosters ON shelters_fosters.foster_id = fosters.foster_id WHERE shelter_id = %s"
    fosterData = (query_ShelterId,)
    fosterList = executeQuery(DBConnect, query, fosterData).fetchall()

    query = "SELECT first_name, last_name, trainers.trainer_id FROM animals_trainers INNER JOIN trainers ON animals_trainers.trainer_id = trainers.trainer_id WHERE animals_trainers.animal_id = %s;"
    resultTrainer = executeQuery(DBConnect, query, data).fetchall()

    query = "SELECT shelters.shelter_name, shelters.shelter_id FROM shelters ORDER BY shelters.shelter_name;"
    sheltersList = executeQuery(DBConnect, query).fetchall()

    #handle for null cage value
    if resultAll[0][3] == None:
        currentCage = ("None",)
    else:
        query = "SELECT cage_name FROM cages WHERE cage_id = %s"
        data = (resultAll[0][3],)
        currentCage = executeQuery(DBConnect, query, data).fetchall()
    
    query = "SELECT cage_name, cage_id FROM cages WHERE shelter_id = %s AND animal_type = %s"
    data = (resultAll[0][11], resultAll[0][5],)
    allCages = executeQuery(DBConnect, query, data).fetchall()

    print(allCages)

    return render_template('animalProfile.html', title='Animals Profile', cageCurrent=currentCage[0][0], cagesList=allCages, allShelters=sheltersList, animal=resultAll[0], foster=fosterResult[0], fosterOptions=fosterList, trainerList=resultTrainer, trainerOptions=possible_trainers)

@app.route("/cages/")
def cages():
    DBConnect = connectDB()

    #Select shelter info for dropdown to input FK
    sheltersQuery = "SELECT shelter_id, shelter_name from shelters"
    sheltersResult = executeQuery(DBConnect, sheltersQuery).fetchall()

    #Select all for list
    query = "SELECT cage_id, shelter_name, cage_location, cage_name, animal_type, capacity, cages.shelter_id FROM `cages` INNER JOIN `shelters` ON cages.shelter_id = shelters.shelter_id;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('cages.html', title='Cages', allCages=result, shelterData=sheltersResult)

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