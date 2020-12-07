from flask import Blueprint, render_template, url_for, request, redirect
from backend.dbConnector import connectDB, executeQuery

sProfile = Blueprint('sProfile', __name__)

# Displays shelter info on profile
@sProfile.route('/shelterProfile/<int:shelterId>')
def shelterProfile(shelterId):
    DBConnect = connectDB()   

    # SELECT for shelter INFO
    shelterQuery = "SELECT * FROM shelters WHERE shelter_id = %s"
    sid = (shelterId,)
    shelterResult = executeQuery(DBConnect, shelterQuery, sid).fetchone()
    rescueGrpQuery = "SELECT rescue_group FROM shelters WHERE shelter_id = %s"
    rescueGrp = executeQuery(DBConnect, rescueGrpQuery, sid).fetchone()
    if rescueGrp == (1,):
        rescueGrp = ('Yes')
    else:
        rescueGrp = ('No')

    # Select trainer info for dropdown to input FK
    trainersFKQuery = "SELECT trainer_id, first_name, last_name  FROM trainers ORDER BY last_name;"
    trainersFKResult = executeQuery(DBConnect, trainersFKQuery).fetchall()

    #Select foster info for dropdown to input FK
    fostersFKQuery = "SELECT foster_id, first_name, last_name  FROM fosters ORDER BY last_name;"
    fostersFKResult = executeQuery(DBConnect, fostersFKQuery).fetchall()

    # shelters_trainers query
    STMMquery = "SELECT shelters_trainers.trainer_id, first_name, last_name FROM `shelters_trainers` INNER JOIN `trainers` ON shelters_trainers.trainer_id = trainers.trainer_id WHERE shelter_id = %s ORDER BY last_name;"
    STMMresult = executeQuery(DBConnect, STMMquery, sid).fetchall()

    # shelters_fosters query
    SFMMquery = "SELECT shelters_fosters.foster_id, first_name, last_name FROM `shelters_fosters` INNER JOIN `fosters` ON shelters_fosters.foster_id = fosters.foster_id WHERE shelter_id = %s ORDER BY last_name;"
    SFMMresult = executeQuery(DBConnect, SFMMquery, sid).fetchall()

    return render_template('shelterProfile.html', title='Shelter Profile', shelter=shelterResult, rescue=rescueGrp, trainersFKData=trainersFKResult, fostersFKData=fostersFKResult, shelterTrainers=STMMresult, shelterFosters=SFMMresult)



@sProfile.route("/shelters/update/<int:id>", methods=["POST"])
def updateShelter(id):
    DBConnect = connectDB()

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
    shelterRescueGrp = request.form['shelterRescueGrp']

    redirectRoute = "/shelterProfile/" + str(id)

    query = "UPDATE shelters SET `shelter_name` = %s, `address_street` = %s, `address_city` = %s, `address_state` = %s, `address_zip` = %s, `animal_quantity` = %s, `cage_quantity` = %s, `total_cage_capacity` = %s, `current_amt_foster_parents` = %s, `current_amt_animals_fostered` = %s, `rescue_group` = %s WHERE shelter_id = %s"
    data = (shelterName, shelterAddress, shelterCity, shelterState, shelterZip, shelterAnimalQuantity, shelterCageQuantity, shelterTotalCageCapacity, shelterCurrAmtFosterParents, shelterCurrAmtAnimalsFostered, shelterRescueGrp, id)
    executeQuery(DBConnect, query, data)
    return redirect(redirectRoute)


@sProfile.route("/shelters/delete/<int:id>", methods=["POST"])
def deleteShelter(id):
    DBConnect = connectDB()

    query = "DELETE FROM shelters WHERE shelter_id = %s"
    data = (id,)
    executeQuery(DBConnect, query, data)
    return redirect("/shelters/")


# ADD to shelters_trainers
@sProfile.route("/shelters-trainers/add", methods=["POST"])
def addSheltersTrainers():
    DBConnect = connectDB()

    shelterID = request.form['shelterID']
    trainerID = request.form['trainerID']
    origin = request.form['origin']

    query = "INSERT INTO shelters_trainers (shelter_id, trainer_id) VALUES (%s, %s)"
    data = (shelterID, trainerID)
    executeQuery(DBConnect, query, data)
    
    if origin == "fromShelterPage":
        redirectRoute = "/shelterProfile/" + shelterID
    elif origin == "fromTrainerPage":
        redirectRoute = "/trainerProfile/" + trainerID
    
    return redirect(redirectRoute)

    
# remove from shelters_trainers
@sProfile.route("/shelters-trainers/delete/<int:id>", methods=["POST"])
def deleteSheltersTrainers(id):
    DBConnect = connectDB()

    shelterID = request.form['shelterID']

    query = "DELETE FROM shelters_trainers WHERE shelter_id = %s AND trainer_id = %s"
    data = (shelterID, id)
    executeQuery(DBConnect, query, data)

    redirectRoute = "/shelterProfile/" + shelterID
    return redirect(redirectRoute)


# ADD to shelters_fosters
@sProfile.route("/shelters-fosters/add", methods=["POST"])
def addSheltersFosters():
    DBConnect = connectDB()

    shelterID = request.form['shelterID']
    fosterID = request.form['fosterID']

    query = "INSERT INTO shelters_fosters (shelter_id, foster_id) VALUES (%s, %s)"
    data = (shelterID, fosterID)
    executeQuery(DBConnect, query, data)

    redirectRoute = "/shelterProfile/" + shelterID
    return redirect(redirectRoute)

    
# remove from shelters_fosters
@sProfile.route("/shelters-fosters/delete/<int:id>", methods=["POST"])
def deleteSheltersFosters(id):
    DBConnect = connectDB()

    shelterID = request.form['shelterID']

    query = "DELETE FROM shelters_fosters WHERE shelter_id = %s AND foster_id = %s"
    data = (shelterID, id)
    executeQuery(DBConnect, query, data)

    redirectRoute = "/shelterProfile/" + shelterID
    return redirect(redirectRoute)