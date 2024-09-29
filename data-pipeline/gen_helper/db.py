from pymongo import MongoClient

import random
from datetime import datetime

def connect_to_mongo():
    mongo_uri_docker = 'mongodb://mongodb:27017/'  # Use the service name 'mongodb' as host
    mongo_uri_local = 'mongodb://localhost:27017/'
    try:
        client = MongoClient(mongo_uri_docker)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("Connected successfully to MongoDB")
        return client
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        return None


def close_mongo_connection(client):
    try:
        client.close()
        print("Connection to MongoDB closed")
    except Exception as e:
        print(f"Could not close connection to MongoDB: {e}")


def list_all_bills(client):
    try:
        db = client['home_dashboard']
        bills_collection = db['bills']
        bills = bills_collection.find()  # Get all records from bills collection
        bills_list = list(bills)  # Convert cursor to list
        for bill in bills_list:
            print(bill)
        return bills_list
    except Exception as e:
        print(f"Error retrieving bills: {e}")
        return None


def write_bill_to_mongo(client, service_provider, amount, month, year):
    try:
        db = client['home_dashboard']
        bills_collection = db['bills']
        bill_document = {
            "service_provider": service_provider,
            "amount": float(amount),  # Changing "bill_amount" to "amount" as per the schema
            "month": month,    # Moving month and year out of the "date" field
            "year": year,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        result = bills_collection.insert_one(bill_document)
        print(f"Bill inserted with id: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting bill into MongoDB: {e}")


def __seed_bills(client):
    for service in ["Brampton Water", "Enbridge", "Alectra", "Reliance Water Heater"]:
        for i in range(1, 10):
            amount = random.randint(50, 200)
            write_bill_to_mongo(client, service, amount, i, 2023)


if __name__ == "__main__":
    client = connect_to_mongo()
    if client:
        print(client.list_database_names())
        # __seed_bills(client)
        list_all_bills(client)
        close_mongo_connection(client)
