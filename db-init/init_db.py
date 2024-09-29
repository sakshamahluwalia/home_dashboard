from pymongo import MongoClient, errors
from bson.decimal128 import Decimal128
import time

def initialize_db():
    max_retries = 10
    retry_interval = 5  # seconds

    mongo_uri = 'mongodb://mongodb:27017/'  # Use the service name 'mongodb' as host

    for attempt in range(max_retries):
        try:
            client = MongoClient(mongo_uri)
            db = client['home_dashboard']

            # Create the 'bills' collection with validation rules
            db.create_collection('bills', validator={
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['service_provider', 'amount', 'month', 'year'],
                    'properties': {
                        'service_provider': {
                            'bsonType': 'string',
                            'description': 'must be a string and is required'
                        },
                        'amount': {
                            'bsonType': ['double', 'decimal'],
                            'description': 'must be a number and is required'
                        },
                        'month': {
                            'bsonType': 'int',
                            'minimum': 1,
                            'maximum': 12,
                            'description': 'must be an integer between 1 and 12 and is required'
                        },
                        'year': {
                            'bsonType': 'int',
                            'description': 'must be an integer and is required'
                        },
                        'created_at': {
                            'bsonType': 'date',
                            'description': 'must be a date if the field exists'
                        },
                        'updated_at': {
                            'bsonType': 'date',
                            'description': 'must be a date if the field exists'
                        }
                    }
                }
            })
            print("Bills collection created.")

            # Create indexes
            db['bills'].create_index(
                [('service_provider', 1), ('year', 1), ('month', 1)],
                unique=True
            )
            print("Indexes created.")

            break  # Exit the retry loop if successful

        except errors.CollectionInvalid:
            print("Bills collection already exists.")
            break  # Exit the retry loop if the collection exists

        except errors.ServerSelectionTimeoutError as e:
            print(f"Attempt {attempt + 1}: MongoDB not ready, retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(retry_interval)
    else:
        print("Failed to connect to MongoDB after multiple attempts.")

if __name__ == "__main__":
    initialize_db()
