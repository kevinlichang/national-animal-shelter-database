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


@fosRoute.route("/fosters/delete/<int:id>", methods=["POST"])
def deleteFoster(id):
    DBConnect = connectDB()

    query = "DELETE FROM fosters WHERE foster_id = %s"
    data = (id,)
    executeQuery(DBConnect, query, data)
    return redirect("/fosters/")