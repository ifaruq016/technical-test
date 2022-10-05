from flask import request, json
from datetime import date, timedelta, datetime
from app import response, app, helpers
from app.connection import db
from bson.json_util import dumps
from uuid import uuid4

def topup():
    try:
        token = request.headers['Authorization']
        token = token.replace('Bearer ', '')

        id = str(uuid4())
        amount = request.json['amount']

        user_collection = db['users']

        validation = helpers.validateToken(token)
        if validation['status'] == '200' :
            cursor = user_collection.find_one({"user_id" : validation['user_id']})
            data_list = json.loads(dumps(cursor))

            if cursor:
                balance_collection = db['balance']
                balance = balance_collection.find_one({"user_id" : validation['user_id']})
                data_balance = json.loads(dumps(balance))

                transaction_collection = db['transaction']
                data_insert_top_up = {
                    "top_up_id" : id,
                    "user_id" : validation['user_id'],
                    "amount_top_up" : amount,
                    "balance_before" : data_balance['balance'],
                    "balance_after" : int(data_balance['balance']) + int(amount),
                    "created_date" : datetime.now()
                }
                insert_data_top_up = transaction_collection.insert_one(data_insert_top_up)
                del data_insert_top_up['_id']

                if insert_data_top_up:
                    data_update_balance = {
                        "user_id" : validation['user_id'],
                        "balance" : data_insert_top_up['balance_after']
                    }
                    update_data = balance_collection.update_one({"user_id": validation['user_id']}, {"$set": data_update_balance})

                return response.resp(200, 'Success', json.loads(dumps(data_insert_top_up)))
            else:
                return response.resp(400, 'Data Not Found', {})
        else:
            return response.resp(401, 'Unauthenticated', {})

    except Exception as e:
        print(e)
        return response.resp(500, 'Error', {})

def payment():
    try:
        token = request.headers['Authorization']
        token = token.replace('Bearer ', '')

        id = str(uuid4())
        amount = request.json['amount']
        remarks = request.json['remarks']

        user_collection = db['users']

        validation = helpers.validateToken(token)
        if validation['status'] == '200' :
            cursor = user_collection.find_one({"user_id" : validation['user_id']})
            data_list = json.loads(dumps(cursor))

            if cursor:
                balance_collection = db['balance']
                balance = balance_collection.find_one({"user_id" : validation['user_id']})
                data_balance = json.loads(dumps(balance))

                if int(data_balance['balance']) > int(amount) :
                    transaction_collection = db['transaction']
                    data_insert_payment = {
                        "payment_id" : id,
                        "user_id" : validation['user_id'],
                        "amount" : amount,
                        "remarks" : remarks,
                        "balance_before" : data_balance['balance'],
                        "balance_after" : int(data_balance['balance']) - int(amount),
                        "created_date" : datetime.now()
                    }
                    insert_data_payment = transaction_collection.insert_one(data_insert_payment)
                    del data_insert_payment['_id']

                    if insert_data_payment:
                        data_update_balance = {
                            "user_id" : validation['user_id'],
                            "balance" : data_insert_payment['balance_after']
                        }
                        update_data = balance_collection.update_one({"user_id": validation['user_id']}, {"$set": data_update_balance})

                    return response.resp(200, 'Success', json.loads(dumps(data_insert_payment)))
                else:
                    return response.resp(400, 'Balance Not Enough', {})
            else:
                return response.resp(404, 'Data Not Found', {})
        else:
            return response.resp(401, 'Unauthenticated', {})

    except Exception as e:
        print(e)
        return response.resp(500, 'Error', {})

def transfer():
    try:
        token = request.headers['Authorization']
        token = token.replace('Bearer ', '')

        id = str(uuid4())
        target_user = request.json['target_user']
        amount = request.json['amount']
        remarks = request.json['remarks']

        user_collection = db['users']

        validation = helpers.validateToken(token)
        if validation['status'] == '200' :
            data_user = user_collection.find_one({"user_id" : validation['user_id']})
            data_list = json.loads(dumps(data_user))

            data_user_target = user_collection.find_one({"user_id" : target_user})
            data_target_list = json.loads(dumps(data_user_target))

            if data_user and data_user_target:
                balance_collection = db['balance']
                balance = balance_collection.find_one({"user_id" : validation['user_id']})
                data_balance = json.loads(dumps(balance))

                if int(data_balance['balance']) > int(amount) :
                    transaction_collection = db['transaction']
                    data_insert_transfer = {
                        "transfer_id" : id,
                        "user_id" : validation['user_id'],
                        "target_user_id" : validation['user_id'],
                        "amount" : amount,
                        "remarks" : remarks,
                        "balance_before" : data_balance['balance'],
                        "balance_after" : int(data_balance['balance']) - int(amount),
                        "created_date" : datetime.now()
                    }
                    insert_data_transfer = transaction_collection.insert_one(data_insert_transfer)
                    del data_insert_transfer['_id']

                    if insert_data_transfer:
                        data_update_balance = {
                            "balance" : data_insert_transfer['balance_after']
                        }
                        update_data = balance_collection.update_one({"user_id": validation['user_id']}, {"$set": data_update_balance})

                        balance = balance_collection.find_one({"user_id" : target_user})
                        data_balance_target = json.loads(dumps(balance))
                        data_update_balance_target = {
                            "balance" : int(data_balance_target['balance']) + int(amount)
                        }
                        update_data = balance_collection.update_one({"user_id": target_user}, {"$set": data_update_balance_target})

                    return response.resp(200, 'Success', json.loads(dumps(data_insert_transfer)))
                else:
                    return response.resp(400, 'Balance Not Enough', {})
            else:
                return response.resp(404, 'Data Not Found', {})
        else:
            return response.resp(401, 'Unauthenticated', {})

    except Exception as e:
        print(e)
        return response.resp(500, 'Error', {})

def report_transaction():
    try:
        token = request.headers['Authorization']
        token = token.replace('Bearer ', '')

        user_collection = db['users']

        validation = helpers.validateToken(token)
        if validation['status'] == '200' :
            data_user = user_collection.find_one({"user_id" : validation['user_id']})
            data_list = json.loads(dumps(data_user))

            if data_user :
                transaction_collection = db['transaction']
                data_transaction = transaction_collection.find({"user_id" : validation['user_id']})
                data_transaction_list = json.loads(dumps(data_transaction))
                for item in data_transaction_list:
                    del item["_id"]

                return response.resp(200, 'Success', data_transaction_list)
            else:
                return response.resp(404, 'Data Not Found', {})
        else:
            return response.resp(401, 'Unauthenticated', {})

    except Exception as e:
        print(e)
        return response.resp(500, 'Error', {})