from config.mysql_config import create_mysql_connection_pool, get_connection_from_pool
import mysql.connector

def save_plan_to_db(user_id, plan_name, plans):
    # Create connection pool
    pool = create_mysql_connection_pool()
    # Connect to MySQL database using the connection pool
    conn = get_connection_from_pool(pool)
    cursor = conn.cursor()

    try:
        # Insert each day's plan into the database
        for plan in plans:
            cursor.execute("""
            """, (
            ))
        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as e:
        print(f"Error inserting data into MySQL: {e}")
        conn.rollback()

    finally:
        # Ensure the connection is closed and returned to the pool
        cursor.close()
        conn.close()
