# run.py

from app import create_app, db

# --- 1. Import the population function ---
# VERIFY THIS PATH: ensure the file is named fillna.py or adjust the import.
from app.services.fillna import populate_all_tables 

# --- Import NoSQL Initialization (Required for clean shutdown) ---
# NOTE: Replace 'app.db.nosql_init' with your actual path to your_db_init.py
try:
    from app.db.nosql_init import cluster # Import the Cassandra cluster object
except ImportError:
    # This prevents the app from failing if you haven't renamed/placed the file yet
    cluster = None 


app = create_app()

# Create tables and populate data inside the application context
with app.app_context():
    # 2. Drop and Create tables
    print("Dropping existing tables...")
    db.drop_all()
    print("Creating new tables...")
    db.create_all()
    
    # --- 3. Call the data population function ---
    print("Starting database population...")
    try:
        populate_all_tables()
        print("Database population complete. 5 rows added to each table.")
    except Exception as e:
        print(f"Error during data population: {e}")
        # Consider a rollback if population fails
        db.session.rollback()

# ===============================================
# CASSANDRA SHUTDOWN (Cleanup)
# ===============================================
# It's crucial to shut down the Cassandra cluster connection cleanly
# after all setup is done but before the application runs or exits.
if cluster:
    try:
        cluster.shutdown()
        print("Cassandra cluster shut down successfully.")
    except Exception as e:
        print(f"Error shutting down Cassandra cluster: {e}")

# ===============================================

if __name__ == "__main__":
    # The application runs only after the setup above is complete
    app.run(host="0.0.0.0", port=5000, debug=True)