from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/regplate", methods = ['POST'])
def get_name():
    form = json.loads(request.data)
    try:
        number = form['number']
        #print(f"name:{number}")
        data = {
            "ABC123" : {
                "owner" : "akasdbkasgbjklgs",
                "id" : None,
                "stolen" : True
            },
            "XYZ789" : {
                "owner" : "John Smith",
                "id" : "#JohnSmithID",
                "stolen" : False
            },
            "FEM555" : {
                "owner" : "Snällbert",
                "id" : "#SnällbertID",
                "stolen" : False
            }
        }
        return data[number]
    except:
        return {"error" : "no such number"}

@app.route("/criminal", methods = ['POST'])
def get_criminal_record():
    form = json.loads(request.data)
    try:
        name = form['name']
        data = {
            "John Smith" : {
                "crimes" : ["burglary", "theft"]
            }
        }
        
        if name in data:
            return data[name]
        return {"crimes" : []}
    except:    
        return {"error" : "bad request"}
    

@app.route("/gunowner", methods = ['POST'])
def get_car_ownership():
    form = json.loads(request.data)
    try:
        name = form['name']
        data = {
            "John Smith" : {
                "gun_owner" : True
            },
            "Snällbert" : {
                "gun_owner" : False
            }
        }
        #print(f"name:{name}")
        return data[name]
    except:
        return {"error" : "bad request"}

@app.route("/asp", methods = ["POST"])
def get_asp_presence():
    form = json.loads(request.data)
    try:
        name = form['name']
        data = {
            "Snällbert" : {
                "in_asp" : True
            }
        }
        
        if name in data:
            return data[name]
        return {"in_asp" : False}
    except:    
        return {"error" : "bad request"}
