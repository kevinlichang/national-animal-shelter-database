from flask import Blueprint, render_template, url_for, request, redirect
from backend.dbConnector import connectDB, executeQuery

testMM = Blueprint('testMM', __name__)

@testMM.route('/shelters-fosters')
def sheltersFosters():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT shelters_fosters.shelter_id, shelter_name, shelters_fosters.foster_id, first_name, last_name FROM `shelters_fosters` INNER JOIN `shelters` ON shelters_fosters.shelter_id = shelters.shelter_id INNER JOIN `fosters` ON shelters_fosters.foster_id = fosters.foster_id ORDER BY last_name;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('shelt-fost-MM.html', title='shelters_fosters_MM', allMM=result)


@testMM.route('/shelters-trainers')
def sheltersTrainers():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT shelters_trainers.shelter_id, shelter_name, shelters_trainers.trainer_id, first_name, last_name FROM `shelters_trainers` INNER JOIN `shelters` ON shelters_trainers.shelter_id = shelters.shelter_id INNER JOIN `trainers` ON shelters_trainers.trainer_id = trainers.trainer_id ORDER BY last_name;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('shelt-train-MM.html', title='shelters_trainers_MM', allMM=result)

@testMM.route('/animals-trainers')
def animalsTrainers():
    DBConnect = connectDB()

    #Select all for list
    query = "SELECT animals_trainers.animal_id, name, animals_trainers.trainer_id, first_name, last_name FROM `animals_trainers` INNER JOIN `animals` ON animals_trainers.animal_id = animals.animal_id INNER JOIN `trainers` ON animals_trainers.trainer_id = trainers.trainer_id ORDER BY last_name;"
    result = executeQuery(DBConnect, query).fetchall()
    return render_template('ani-train-MM.html', title='animals_trainers_MM', allMM=result)
