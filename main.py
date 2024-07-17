from pymongo import MongoClient, errors
from bson.objectid import ObjectId


connection = "mongodb+srv://shata:landROua25@cluster0.pcvxugf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
client = MongoClient(connection)


db = client["cat_database"]
collection = db["cats"]


default_cat = {
    "name": "barsik",
    "age": 3,
    "features": ["ходить в капці", "дає себе гладити", "рудий"]
}


def create_cat(cat):
    """Add new cat"""
    try:
        result = collection.insert_one(cat)
        print(f"Cat added")
    except errors.PyMongoError as e:
        print(f"Error: {e}")


def read_all_cats():
    """Read all cats"""
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print(f"Error reading record: {e}")


def read_cat_by_name(name):
    """Displays information about the cat by name"""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"cat {name} not found.")
    except errors.PyMongoError as e:
        print(f"Error reading record: {e}")


def update_cat_age(name, new_age):
    """Update cat age"""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Cats {name} age update to {new_age}.")
        else:
            print(f"Cat {name} not found or age didnt update")
    except errors.PyMongoError as e:
        print(f"Error age updating: {e}")


def add_feature_to_cat(name, feature):
    """Add new feature"""
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count > 0:
            print(f"Feature'{feature}' add to {name}.")
        else:
            print(f"Cat {name} not found or feature already exist.")
    except errors.PyMongoError as e:
        print(f"Add feature error: {e}")


def delete_cat_by_name(name):
    """Delete cat"""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Cat {name} deleted")
        else:
            print(f"Cat {name} not found")
    except errors.PyMongoError as e:
        print(f"Delete error: {e}")


def delete_all_cats():
    """Delete all records"""
    try:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} records")
    except errors.PyMongoError as e:
        print(f"Delete error: {e}")

if __name__ == "__main__":
    create_cat(default_cat)
    read_all_cats()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 8)
    add_feature_to_cat("barsik", "Бандит-рецидивіст")
    # delete_cat_by_name("barsik")
    # delete_all_cats()
