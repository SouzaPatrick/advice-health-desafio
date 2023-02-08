import os

from app import create_app
from app.database import create_db_and_tables
from app.db_function import create_user_test

# Remove SQLite DB
sqlite_db: str = "database.db"
# If file exists, delete it.
if os.path.isfile(sqlite_db):
    os.remove(sqlite_db)

# Create DB
app = create_app()
with app.app_context():
    create_db_and_tables()

    # Create user test
    create_user_test()

print("DB successfully reset")
print("Create user test: 'username'='advicehealth' 'password'='advicehealth'")
print("Authentication through Basic Auth")
