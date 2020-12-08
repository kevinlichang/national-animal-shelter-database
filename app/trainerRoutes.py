from flask import Blueprint, render_template, url_for, request, redirect
from backend.dbConnector import connectDB, executeQuery

trainRoute = Blueprint('trainRoute', __name__)

@trainRoute.route('/trainers/')
def trainers():
    DBConnect = connectDB()

    #Select query for shelterFKs
    sFKQuery = "SELECT shelter_id, shelter_name, address_city, address_state FROM shelters ORDER BY address_state;"
    sFKResult = executeQuery(DBConnect, sFKQuery).fetchall()
    
    

    #Select all for list
    query = "SELECT * FROM trainers ORDER BY last_name"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('trainers.html', title='Trainers', allTrainers=result, sheltersData=sFKResult)


@trainRoute.route('/trainers/', methods=["POST"])
def addTrainer():
    DBConnect = connectDB()

    #data from addTrainerForm
    trainerFName = request.form['trainerFName']
    trainerLName = request.form['trainerLName']
    trainerSpecialty = request.form['trainerSpecialty']

    query = "INSERT INTO `trainers` (`first_name`, `last_name`, `animal_specialty`) VALUES (%s, %s, %s)"
    data = (trainerFName, trainerLName, trainerSpecialty)
    executeQuery(DBConnect, query, data)

    #data for shelterTrainer MM relationship
    trainerShelterID = request.form['trainerShelterID']

    if trainerShelterID != " ":
        addNewTrainerShelterMM(trainerShelterID, trainerFName, trainerLName)
    return redirect('/trainers/')


#   Add new row into shelters_trainers MM table
def addNewTrainerShelterMM(shelterID, trainerFName, trainerLName):
    DBConnect = connectDB()

    #INSERT into shelters_trainers_MM
    query = "INSERT INTO `shelters_trainers` (shelter_id, trainer_id) VALUES (%s, (SELECT trainer_id FROM trainers WHERE first_name = %s AND last_name = %s ORDER BY trainer_id DESC LIMIT 1))"
    data = (shelterID, trainerFName, trainerLName)
    executeQuery(DBConnect, query, data)


#   Add new row into shelters_trainers MM table
def addNewTrainerShelterMM(shelterID, trainerFName, trainerLName):
    DBConnect = connectDB()

    #INSERT into shelters_trainers_MM
    query = "INSERT INTO `shelters_trainers` (shelter_id, trainer_id) VALUES (%s, (SELECT trainer_id FROM trainers WHERE first_name = %s AND last_name = %s ORDER BY trainer_id DESC LIMIT 1))"
    data = (shelterID, trainerFName, trainerLName)
    executeQuery(DBConnect, query, data)

@trainRoute.route("/trainers/delete/<int:id>", methods=["POST"])
def deleteTrainer(id):
    DBConnect = connectDB()

    query = "DELETE FROM trainers WHERE trainer_id = %s"
    data = (id,)
    executeQuery(DBConnect, query, data)
    query = "DELETE FROM animals_trainers WHERE trainer_id = %s"
    executeQuery(DBConnect, query, data)
    query = "DELETE FROM shelters_animals WHERE trainer_id = %s"
    executeQuery(DBConnect, query, data)
    return redirect("/trainers/")

# Displays trainer info on Profile
@trainRoute.route("/trainerProfile/<int:trainerId>")
def trainerProfile(trainerId):
    DBConnect = connectDB()   

    #Select trainer info
    trainerQuery = "SELECT * FROM trainers WHERE trainer_id = %s"
    tid = (trainerId,)
    trainerResult = executeQuery(DBConnect, trainerQuery, tid).fetchone()

    #Select query for animalsFK's
    animalsFKQuery = "SELECT animal_id, name FROM animals ORDER BY name"
    animalsFKResult = executeQuery(DBConnect, animalsFKQuery).fetchall()

    # Select trainer info for dropdown to input FK
    sheltersFKQuery = "SELECT shelter_id, shelter_name, address_street, address_city, address_state, address_zip FROM shelters ORDER BY address_state;"
    sheltersFKResult = executeQuery(DBConnect, sheltersFKQuery).fetchall()

    # trainers_shelters query
    TSMMquery = "SELECT shelters_trainers.shelter_id, shelter_name, address_street, address_city, address_state, address_zip FROM `shelters_trainers` INNER JOIN `shelters` ON shelters_trainers.shelter_id = shelters.shelter_id WHERE trainer_id = %s ORDER BY address_state;"
    TSMMresult = executeQuery(DBConnect, TSMMquery, tid).fetchall()

    # trainers_animals query
    TAMMquery = "SELECT animals.animal_id, animals.name FROM animals_trainers INNER JOIN animals ON animals_trainers.animal_id = animals.animal_id WHERE animals_trainers.trainer_id = %s ORDER BY animals.name;"
    TAMMquery = executeQuery(DBConnect, TAMMquery, tid).fetchall()

    return render_template('trainerProfile.html', title='Trainer Profile', animalsFKData=animalsFKResult, trainerAnimals=TAMMquery, trainer=trainerResult, sheltersFKData=sheltersFKResult,  trainerShelters=TSMMresult)

# remove from shelters_trainers
@trainRoute.route("/trainers-shelters/delete/<int:id>", methods=["POST"])
def deleteTrainersShelters(id):
    DBConnect = connectDB()

    trainerID = request.form['trainerID']

    query = "DELETE FROM shelters_trainers WHERE shelter_id = %s AND trainer_id = %s"
    data = (id, trainerID )
    executeQuery(DBConnect, query, data)

    redirectRoute = "/trainerProfile/" + trainerID
    return redirect(redirectRoute)

@trainRoute.route("/trainers-animals/delete/<int:id>", methods=["POST"])
def deleteTrainersAnimals(id):
    DBConnect = connectDB()

    trainerID = request.form['trainerID']

    query = "DELETE FROM animals_trainers WHERE animal_id = %s AND trainer_id = %s"
    data = (id, trainerID )
    executeQuery(DBConnect, query, data)

    redirectRoute = "/trainerProfile/" + trainerID
    return redirect(redirectRoute)

@trainRoute.route("/animal-trainers/add", methods=["POST"])
def addTrainersAnimals():
    DBConnect = connectDB()

    trainerID = request.form['trainerID']
    animalID = request.form['animalID']

    query = "INSERT INTO `animals_trainers`(`animal_id`, `trainer_id`) VALUES (%s, %s);"
    data = (animalID, trainerID)
    executeQuery(DBConnect, query, data)
    return redirect('/trainerProfile/%s'%(trainerID))