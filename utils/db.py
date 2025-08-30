import sqlite3
from utils.logger import log


class Database:
    """
    A class to handle SQLite database operations for the chatbot.
    """

    def __init__(self, db_name="db/chatbot_history.db"):
        """
        Initializes the Database class and creates the conversations table if it doesn't exist.

        Args:
            db_name (str): The name of the database file.
        """
        try:
            # The check_same_thread=False argument is important for multi-threaded applications
            # like Streamlit to prevent threading issues with SQLite.
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            log.error(f"Database connection error: {e}")

    def create_table(self):
        """
        Creates the 'conversations' table if it does not exist.
        """
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            self.conn.commit()
            log.info("Database table 'conversations' is ready.")
        except sqlite3.Error as e:
            log.error(f"Error creating table: {e}")

    def insert_conversation(self, user_id, role, content):
        """
        Inserts a message into the conversations table.

        Args:
            user_id (str): The unique identifier for the user session.
            role (str): The role of the message sender (e.g., 'user' or 'assistant').
            content (str): The content of the message.
        """
        try:
            self.cursor.execute(
                """
                INSERT INTO conversations (user_id, role, content)
                VALUES (?, ?, ?)
            """,
                (user_id, role, content),
            )
            self.conn.commit()
            log.info(f"Inserted message for user_id: {user_id}")
        except sqlite3.Error as e:
            log.error(f"Error inserting conversation: {e}")

    def fetch_conversation_history(self, user_id):
        """
        Fetches the conversation history for a specific user_id.

        Args:
            user_id (str): The unique identifier for the user session.

        Returns:
            list: A list of tuples, where each tuple represents a message in the conversation.
                  Returns an empty list if no history is found or an error occurs.
        """
        try:
            self.cursor.execute(
                """
                SELECT role, content FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp ASC
            """,
                (user_id,),
            )
            history = self.cursor.fetchall()
            log.info(f"Fetched {len(history)} messages for user_id: {user_id}")
            return history
        except sqlite3.Error as e:
            log.error(f"Error fetching conversation history for user_id {user_id}: {e}")
            return []

    def delete_conversation_history(self, user_id):
        """
        Deletes the entire conversation history for a specific user_id.

        Args:
            user_id (str): The unique identifier for the user session whose history will be deleted.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            self.cursor.execute(
                """
                DELETE FROM conversations
                WHERE user_id = ?
            """,
                (user_id,),
            )
            self.conn.commit()
            # The rowcount attribute returns the number of rows affected by the last operation.
            if self.cursor.rowcount > 0:
                log.info(
                    f"Successfully deleted {self.cursor.rowcount} messages for user_id: {user_id}"
                )
            else:
                log.warning(
                    f"No conversation history found to delete for user_id: {user_id}"
                )
            return True
        except sqlite3.Error as e:
            log.error(f"Error deleting conversation history for user_id {user_id}: {e}")
            return False

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
            log.info("Database connection closed.")
