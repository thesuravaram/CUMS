# your_db_init.py (Refactored)

from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime
import traceback
import sys

# Global variables (Initialized to None)
mongo_client = None
mongo_collection = None
cluster = None
session = None

# ==============================
# Connection Functions (MUST BE CALLED EXPLICITLY)
# ==============================

def init_mongodb():
    """Initializes and sets the global MongoDB collection object."""
    global mongo_client, mongo_collection
    try:
        mongo_client = MongoClient("mongodb://admin:admin123@localhost:27017", serverSelectionTimeoutMS=5000)
        mongo_client.admin.command('ismaster') 
        
        mongo_db = mongo_client["university_db"]
        mongo_collection = mongo_db["student_documents"]
        print("MongoDB connection established and collection ready.")
        
    except Exception as e:
        print("\n--- MongoDB Connection FAILED ---", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        mongo_collection = None


def init_cassandra():
    """Initializes the Cassandra session, keyspace, and table."""
    global cluster, session
    
    # 1. Attempt connection setup
    try:
        auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra123')
        cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
        session = cluster.connect() # This sets the global session variable
    except Exception:
        # If connection fails, cluster/session are unusable.
        print("\n--- Cassandra Connection FAILED (at Cluster.connect) ---", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        session = None
        return # Exit: Leave session as None

    # 2. Attempt DDL/Schema setup (Only runs if connection succeeded)
    try:
        KEYSPACE = 'documents'
        TABLE = 'student_files'

        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}
        """)

        session.set_keyspace(KEYSPACE)

        session.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                doc_id UUID PRIMARY KEY,
                student_id int,
                file_name text,
                file_data blob,
                upload_date timestamp
            )
        """)
        
        # SUCCESS PATH
        print("Cassandra connection established and schema verified.")
        # NO RETURN STATEMENT HERE. The global 'session' variable remains set from the try block above.
        
    except Exception:
        # If DDL fails (after connecting), print error and set global session to None
        print("\n--- Cassandra Schema Setup FAILED ---", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        session = None # This overrides the successful connection with None
# ==============================
# REMOVED: Immediate execution lines like 'mongo_collection = init_mongodb()'
# The caller (create_app) will now execute these functions.
# ==============================

__all__ = ['mongo_collection', 'session', 'cluster', 'init_mongodb', 'init_cassandra']