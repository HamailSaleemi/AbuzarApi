import pyodbc
import config_sql


class SQLConnection:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(config_sql.conn_str)
            self.cursor = self.conn.cursor()  # Create a cursor for executing queries
            print(f'Database "{config_sql.database}" connected successfully')
        except Exception as e:
            print(f"Error: {e}")

    def execute_query(self, query):
        """Execute a SQL query and return the result."""
        try:
            self.cursor.execute(query)
            self.conn.commit()  # Commit changes if it's an INSERT, UPDATE, DELETE query
            return self.cursor.fetchall()  # Return fetched results if it's a SELECT query
        except Exception as e:
            print(f"Query Execution Error: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed")