from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/regplate", methods = ['POST'])
def get_name():
    #number = request.form['number']
    #print(f"name:{number}")
    return {"owner" : "Patrik Guthenberg", "stolen" : False}

@app.route("/criminal", methods = ['POST'])
def get_criminal_record():
    #name = request.form['name']
    #print(f"name:{name}")
    return {"in_record" : True, "crime_info": {"crime" : "Murder", "date" : "2022-12-06"}}

@app.route("/gunowner", methods = ['POST'])
def get_car_ownership():
    #name = request.form['name']
    #print(f"name:{name}")
    return {"owns_gund" : True}

