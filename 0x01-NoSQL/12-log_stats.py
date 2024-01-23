#!/usr/bin/env python3
"""
This script provides some stats about Nginx logs stored in MongoDB
"""
import pymongo


methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

if __name__ == "__main__":

    client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    nginx_collection = None
    if "logs" in client.list_database_names() and \
            "nginx" in client.logs.list_collection_names():
        nginx_collection = client.logs.nginx
    if nginx_collection is not None:
        print("{} logs".format(nginx_collection.count_documents({})))
        print("Methods:")
        for method in methods:
            print("\tmethod {}: {}".format(
                method,
                nginx_collection.count_documents({"method": method}))
                )
        print("{} status check".format(
            nginx_collection.count_documents({
                "method": "GET",
                "path": "/status"
                })))
