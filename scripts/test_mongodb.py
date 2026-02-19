#!/usr/bin/env python
"""Test MongoDB connection and show configuration options."""

import os
import sys

# Add project to path
sys.path.insert(0, r'd:\p\e-learning_project_django\django-courses')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseproject.settings')

import django
django.setup()

from mongoengine import connect, disconnect
from pymongo import MongoClient

print("=" * 60)
print("MongoDB Connection Test")
print("=" * 60)

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/elearning_mongo")
mongo_db = os.getenv("MONGO_DB_NAME", "elearning_mongo")

print(f"\n📍 Current MongoDB URI: {mongo_uri}")
print(f"📍 Current Database Name: {mongo_db}")

# Try to connect
try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Force connection attempt
    client.admin.command('ping')
    print("\n✅ MongoDB Connection: SUCCESS!")
    print(f"   Server Info: {client.server_info()['version']}")
    
    # List databases
    db_list = client.list_database_names()
    print(f"\n📊 Available Databases: {db_list}")
    
    client.close()
    
except Exception as e:
    print(f"\n❌ MongoDB Connection: FAILED")
    print(f"   Error: {e}")
    print("\n💡 Troubleshooting Options:")
    print("   1. Start MongoDB locally:")
    print("      - Windows: net start MongoDB (if installed)")
    print("      - or download from https://www.mongodb.com/try/download/community")
    print("\n   2. Use MongoDB Atlas (Cloud):")
    print("      - Create account at https://www.mongodb.com/cloud/atlas")
    print("      - Get connection string from Atlas")
    print("      - Set env var: MONGO_URI='<your-atlas-connection-string>'")
    print("\n   3. Update .env file with your MongoDB connection details")

print("\n" + "=" * 60)
print("Configuration Help:")
print("=" * 60)
print("\nOption A: Local MongoDB")
print("-" * 60)
print("1. Install MongoDB Community: https://docs.mongodb.com/manual/installation/")
print("2. Start MongoDB service:")
print("   - Windows: mongod (or 'net start MongoDB')")
print("   - Should run on localhost:27017 by default")
print("3. Default connection string works as-is")
print("\nOption B: MongoDB Atlas (Cloud)")
print("-" * 60)
print("1. Go to https://www.mongodb.com/cloud/atlas")
print("2. Create free tier cluster")
print("3. Get connection string (looks like):")
print("   mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority")
print("4. Create or update .env file with:")
print("   MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/elearning_mongo")
print("   MONGO_DB_NAME=elearning_mongo")
print("\n" + "=" * 60)
