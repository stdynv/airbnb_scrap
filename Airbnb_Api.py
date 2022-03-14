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

@app.route('/<destination>',methods = ['GET'])
def get_item(destination):
    
    try : 
        data = list(db.get_collection(destination).find())
        for d in data :
            d['_id'] = str(d['_id'])

        return Response(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    except Exception as ex:
        print(ex)

@app.route('/<destination>/add',methods = ['POST'])
def add_item(destination):
    try : 
        data = {'Title' : request.form['title'] ,
                'Description' :request.form['description'],
                 'Type of Rooms' : request.form['rooms'],
                 'Allowed Guests' : int(request.form['guests']),
                 'Details Proprety' : request.form['proprety'],
                 'Price per Night' : int(request.form['price']),
                 'Link' : request.form['link']
                 }
        db_response = db.get_collection(destination).insert_one(data)
        return Response(
            response=json.dumps({'message':f'record created on {destination}' , 'id':f'{db_response.inserted_id}'}),
            status=200,
            mimetype='application/json'
        )
    except Exception as ex:
        print(ex)

@app.route('/update/<destination>/<id>',methods = ['PATCH'])
def update_item(destination,id):

    try : 
        
        db_response = db.get_collection(destination).update_many(
            {'_id' : ObjectId(id)},
            {'$set':{
                'Title' : request.form['title'] ,
                'Description' :request.form['description'],
                 'Type of Rooms' : request.form['rooms'],
                 'Allowed Guests' : int(request.form['guests']),
                 'Details Proprety' : request.form['proprety'],
                 'Price per Night' : int(request.form['price']),
                 'Link' : request.form['link']
                }
            }
        )
        if db_response.modified_count == 1 :
            return Response(
                response=json.dumps({f'message':'record  updated'}),
                status=200,
                mimetype='application/json'
            )
    except Exception as ex:
        print(ex)

@app.route('/delete/<destination>/<id>',methods = ['DELETE'])
def delete_item(destination,id):

    try : 
        # user = {'first_name' : request.form['first_name'] ,'last_name' :request.form['last_name'] }
        db_response = db.get_collection(destination).delete_one(
            {'_id' : ObjectId(id)})

        if db_response.deleted_count == 1 :
            return Response(
                response=json.dumps({'message':'record  deleted'}),
                status=200,
                mimetype='application/json'
            )
        return Response(
                response=json.dumps({'message':'record  not found'}),
                status=500,
                mimetype='application/json'
                )

        
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    app.run(debug=True)

