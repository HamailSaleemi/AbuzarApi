import pyodbc
from AbuzarApi.DATABASE import config_sql


class SQLConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect_db()  # Create a persistent connection

    def connect_db(self):
        """Establish a persistent database connection."""
        if self.conn is None:
            try:
                self.conn = pyodbc.connect(config_sql.conn_str)
                self.cursor = self.conn.cursor()
                print(f'✅ Database "{config_sql.database}" connected successfully')
            except Exception as e:
                print(f"❌ Connection Error: {e}")

    def execute_query(self, query, params=None):
        """Execute a SQL query and return results if applicable."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Commit only for write queries
            if query.strip().lower().startswith(("insert", "update", "delete")):
                self.conn.commit()
                return None  # No results for write queries

            return self.cursor.fetchall()  # Fetch results only for SELECT
        except Exception as e:
            print(f"❌ Query Execution Error: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print("✅ Database connection closed")

    def get_cursor(self):
        """Return the cursor for direct execution."""
        return self.cursor


# Create a single persistent connection instance
SQL_CONN = SQLConnection()
