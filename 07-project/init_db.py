from dotenv import load_dotenv

from app.db import initialize_db


_ = load_dotenv()


if __name__ == "__main__":
    print("Initializing database...")
    initialize_db()
    print("Database initialized.")
