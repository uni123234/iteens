def create_default_tables(cursor, conn):
    """
    Creates default tables in the database if they do not exist.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute SQL commands.
        conn (sqlite3.Connection): The connection to the database.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(32) NOT NULL,
            first_name VARCHAR(256),
            last_name VARCHAR(256),
            lng_lvl VARCHAR(2),
            telegram_id INTEGER,
            progress INTEGER 
        );       
    """)
    conn.commit()
