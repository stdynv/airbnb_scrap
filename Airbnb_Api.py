from flask import Flask , Response, request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try :
    # connect to mongodb
    mongo = pymongo.MongoClient(
        host='localhost',
        port=27017,
        serverSelectionTimeoutMS = 1000)
    mongo.server_info()
    
    # database 

    db = mongo.airbnb

except Exception :
    print('Error cannot connect to db ')


@app.route('/',methods = ['GET'])
def get_item():
    
    try : 
        data = list(db.Paris.find())
        for d in data :
            d['_id'] = str(d['_id'])

        return Response(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    except Exception as ex:
        print(ex)

@app.route('/add',methods = ['POST'])
def add_item():
    try : 
        data = {'Title' : request.form['title'] ,
                'Description' :request.form['description'],
                 'Type of Rooms' : request.form['rooms'],
                 'Allowed Guests' : int(request.form['guests']),
                 'Price per Night' : int(request.form['price'])
                 }
        db_response = db.Paris.insert_one(data)
        return Response(
            response=json.dumps({'message':'record created' , 'id':f'{db_response.inserted_id}'}),
            status=200,
            mimetype='application/json'
        )
    except Exception as ex:
        print(ex)

@app.route('/update/<id>',methods = ['PATCH'])
def update_item(id):

    try : 
        # user = {'first_name' : request.form['first_name'] ,'last_name' :request.form['last_name'] }
        db_response = db.Paris.update_many(
            {'_id' : ObjectId(id)},
            {'$set':{
                'Title' : request.form['title'] ,
                'Description' :request.form['description'],
                 'Type of Rooms' : request.form['rooms'],
                 'Allowed Guests' : int(request.form['guests']),
                 'Price per Night' : int(request.form['price'])
                }
            }
        )
        if db_response.modified_count == 1 :
            return Response(
                response=json.dumps({'message':'record  updated'}),
                status=200,
                mimetype='application/json'
            )
    except Exception as ex:
        print(ex)

@app.route('/delete/<id>',methods = ['DELETE'])
def delete_item(id):

    try : 
        # user = {'first_name' : request.form['first_name'] ,'last_name' :request.form['last_name'] }
        db_response = db.Paris.delete_one(
            {'_id' : ObjectId(id)})

        if db_response.deleted_count == 1 :
            return Response(
                response=json.dumps({'message':'record  deleted'}),
                status=200,
                mimetype='application/json'
            )
        return Response(
                response=json.dumps({'message':'record  not found'}),
                status=200,
                mimetype='application/json'
                )

        
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    app.run(debug=True)

