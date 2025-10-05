import sqlite3
from src.common.logger import log
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    """
    A class to handle SQLite database operations for the chatbot,
    including user authentication and conversation history.
    """

    def __init__(self, db_name="db/chatbot_history.db"):
        """
        Initializes the Database class and creates necessary tables.
        """
        try:
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            # Create both tables on initialization
            self.create_conversations_table()
            self.create_users_table()
        except sqlite3.Error as e:
            log.error(f"Database connection error: {e}")

    def create_users_table(self):
        """Creates the 'users' table if it does not exist."""
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """
            )
            self.conn.commit()
            log.info("Database table 'users' is ready.")
        except sqlite3.Error as e:
            log.error(f"Error creating users table: {e}")

    def create_conversations_table(self):
        """Creates the 'conversations' table if it does not exist."""
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            self.conn.commit()
            log.info("Database table 'conversations' is ready.")
        except sqlite3.Error as e:
            log.error(f"Error creating conversations table: {e}")

    def add_user(self, username, password):
        """Adds a new user to the database with a hashed password."""
        try:
            # Generate a secure hash of the password
            password_hash = generate_password_hash(password)
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            self.conn.commit()
            log.info(f"User '{username}' created successfully.")
            return True
        except sqlite3.IntegrityError:
            # This error occurs if the username is already taken
            log.warning(f"Attempted to create a user that already exists: {username}")
            return False
        except sqlite3.Error as e:
            log.error(f"Error adding user {username}: {e}")
            return False

    def verify_user(self, username, password):
        """Verifies a user's credentials against the stored hash."""
        try:
            self.cursor.execute(
                "SELECT password_hash FROM users WHERE username = ?", (username,)
            )
            result = self.cursor.fetchone()
            if result:
                password_hash = result[0]
                # Check if the provided password matches the stored hash
                if check_password_hash(password_hash, password):
                    log.info(f"User '{username}' authenticated successfully.")
                    return True
            log.warning(f"Failed authentication attempt for user '{username}'.")
            return False
        except sqlite3.Error as e:
            log.error(f"Error verifying user {username}: {e}")
            return False

    def insert_conversation(self, username, role, content):
        """Inserts a message into the conversations table, linked to a username."""
        try:
            self.cursor.execute(
                """
                INSERT INTO conversations (username, role, content)
                VALUES (?, ?, ?)
            """,
                (username, role, content),
            )
            self.conn.commit()
            log.info(f"Inserted message for user: {username}")
        except sqlite3.Error as e:
            log.error(f"Error inserting conversation: {e}")

    def fetch_conversation_history(self, username):
        """Fetches the conversation history for a specific username."""
        try:
            self.cursor.execute(
                """
                SELECT role, content FROM conversations
                WHERE username = ?
                ORDER BY timestamp ASC
            """,
                (username,),
            )
            history = self.cursor.fetchall()
            log.info(f"Fetched {len(history)} messages for user: {username}")
            # Convert list of tuples to list of dicts for session state
            return [{"role": role, "content": content} for role, content in history]
        except sqlite3.Error as e:
            log.error(f"Error fetching conversation history for user {username}: {e}")
            return []

    # delete_conversation_history can remain the same, just ensure it uses 'username'
    def delete_conversation_history(self, username):
        """Deletes the entire conversation history for a specific username."""
        try:
            self.cursor.execute(
                "DELETE FROM conversations WHERE username = ?", (username,)
            )
            self.conn.commit()
            if self.cursor.rowcount > 0:
                log.info(f"Deleted history for user: {username}")
            return True
        except sqlite3.Error as e:
            log.error(f"Error deleting history for user {username}: {e}")
            return False

    def close_connection(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            log.info("Database connection closed.")
