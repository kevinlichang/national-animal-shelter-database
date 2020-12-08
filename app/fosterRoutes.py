from flask import Blueprint, render_template, url_for, request, redirect
from backend.dbConnector import connectDB, executeQuery

fosRoute = Blueprint('fosRoute', __name__)

@fosRoute.route('/fosters/')
def fosters():
    DBConnect = connectDB()

    #Select query for shelterFKs
    sFKQuery = "SELECT shelter_id, shelter_name, address_city, address_state FROM shelters ORDER BY address_state;"
    sFKResult = executeQuery(DBConnect, sFKQuery).fetchall()

    #Select all for list
    query = "SELECT * FROM fosters ORDER BY last_name"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('fosters.html', title='Fosters', allFosters=result, sheltersData=sFKResult)


@fosRoute.route('/fosters/', methods=["POST"])
def addFoster():
    DBConnect = connectDB()

    #data from addfosterForm
    fosterFName = request.form['fosterFName']
    fosterLName = request.form['fosterLName']
    fosterDriverLicense = request.form['fosterDriverLicense']
    fosterPhone = request.form['fosterPhone']
    fosterAddress = request.form['fosterAddress']
    fosterCity = request.form['fosterCity']
    fosterState = request.form['fosterState']
    fosterZip = request.form['fosterZip']

    query = "INSERT INTO `fosters` (`first_name`, `last_name`, `license_num`, `phone`, `address_street`, `address_city`, `address_state`, `address_zip`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
    data = (fosterFName, fosterLName, fosterDriverLicense, fosterPhone, fosterAddress, fosterCity, fosterState, fosterZip)
    executeQuery(DBConnect, query, data)

    #data for shelterfoster MM relationship
    fosterShelterID = request.form['fosterShelterID']

    if fosterShelterID != " ":
        addNewFosterShelterMM(fosterShelterID, fosterFName, fosterLName)
    return redirect('/fosters/')


@fosRoute.route("/fosters/delete/<int:id>", methods=["POST"])
def deleteFoster(id):
    DBConnect = connectDB()

    query = "DELETE FROM fosters WHERE foster_id = %s"
    data = (id,)
    executeQuery(DBConnect, query, data)
    return redirect("/fosters/")

#   Add new row into shelters_fosters MM table
def addNewFosterShelterMM(shelterID, fosterFName, fosterLName):
    DBConnect = connectDB()

    #INSERT into shelters_fosters_MM
    query = "INSERT INTO `shelters_fosters` (shelter_id, foster_id) VALUES (%s, (SELECT foster_id FROM fosters WHERE first_name = %s AND last_name = %s ORDER BY foster_id DESC LIMIT 1))"
    data = (shelterID, fosterFName, fosterLName)
    executeQuery(DBConnect, query, data)

# Displays foster info on Profile
@fosRoute.route("/fosterProfile/<int:fosterId>")
def fosterProfile(fosterId):
    DBConnect = connectDB()   

    #Select foster info
    fosterQuery = "SELECT * FROM fosters WHERE foster_id = %s"
    fid = (fosterId,)
    fosterResult = executeQuery(DBConnect, fosterQuery, fid).fetchone()


    # Select foster info for dropdown to input FK
    sheltersFKQuery = "SELECT shelter_id, shelter_name, address_street, address_city, address_state, address_zip FROM shelters ORDER BY address_state;"
    sheltersFKResult = executeQuery(DBConnect, sheltersFKQuery).fetchall()

    # fosters_shelters query
    FSMMquery = "SELECT shelters_fosters.shelter_id, shelter_name, address_street, address_city, address_state, address_zip FROM `shelters_fosters` INNER JOIN `shelters` ON shelters_fosters.shelter_id = shelters.shelter_id WHERE foster_id = %s ORDER BY address_state;"
    FSMMresult = executeQuery(DBConnect, FSMMquery, fid).fetchall()


    return render_template('fosterProfile.html', title='Foster Profile', foster=fosterResult, sheltersFKData=sheltersFKResult,  fosterShelters=FSMMresult)


# remove from shelters_fosters
@fosRoute.route("/fosters-shelters/delete/<int:id>", methods=["POST"])
def deleteFostersShelters(id):
    DBConnect = connectDB()

    fosterID = request.form['fosterID']

    query = "DELETE FROM shelters_fosters WHERE shelter_id = %s AND foster_id = %s"
    data = (id, fosterID )
    executeQuery(DBConnect, query, data)

    redirectRoute = "/fosterProfile/" + fosterID
    return redirect(redirectRoute)