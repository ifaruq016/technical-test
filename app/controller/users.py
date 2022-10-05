from flask import request, json
from datetime import date, timedelta, datetime
from app import response, app, helpers
from app.connection import db
from bson.json_util import dumps
from uuid import uuid4

# Register New User
def register():
    try:
        id = str(uuid4())
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        phone_number = request.json['phone_number']
        pin = request.json['pin']
        address = request.json['address']

        user_collection = db['users']
        cursor = user_collection.find_one({"phone_number" : phone_number})
        data_response = {}
        if cursor:
            return response.resp(200, 'Phone Number already registered', data_response)
        else:
            data_insert = {
                "user_id" : id,
                "first_name" : first_name,
                "last_name" : last_name,
                "phone_number" : phone_number,
                "pin" : pin,
                "address" : address
            }
            insert_data = user_collection.insert_one(data_insert)
            del data_insert['_id']

            return response.resp(200, 'Success', json.loads(dumps(data_insert)))

    except Exception as e:
        print(e)
        return response.resp(500, 'Error', {})

def login():
    try:
        phone_number = request.json['phone_number']
        pin = request.json['pin']
        data_response = {}

        user_collection = db['users']
        cursor = user_collection.find_one({"phone_number" : phone_number})
        data_list = json.loads(dumps(cursor))

        if cursor:
            if data_list['pin'] == pin:
                data_response = {
                    "access_token" : helpers.jwtEncode(data_list),
                    "refresh_token" : helpers.jwtEncode(data_list)
                }

                return response.resp(200, 'Success', json.loads(dumps(data_response)))
            else:
                return response.resp(400, 'Phone number or pin not match', data_response)

    except Exception as e:
        print(e)
        return response.resp(500, 'Error', {})

def update_profile():
    try:
        token = request.headers['Authorization']
        token = token.replace('Bearer ', '')

        first_name = request.json['first_name']
        last_name = request.json['last_name']
        phone_number = request.json['phone_number']
        address = request.json['address']

        user_collection = db['users']

        validation = helpers.validateToken(token)
        if validation['status'] == '200' :
            cursor = user_collection.find_one({"user_id" : validation['user_id']})
            data_list = json.loads(dumps(cursor))

            if cursor:
                data_update = {
                    "user_id" : validation['user_id'],
                    "first_name" : first_name,
                    "last_name" : last_name,
                    "phone_number" : phone_number,
                    "address" : address
                }
                update_data = user_collection.update_one({"user_id": validation['user_id']}, {"$set": data_update})
                print(update_data)

                return response.resp(200, 'Success', json.loads(dumps(data_update)))
            else:
                return response.resp(400, 'Data Not Found', {})


        return response.resp(200, 'Success', {})

    except Exception as e:
        print(e)
        return response.resp(500, 'Error', {})