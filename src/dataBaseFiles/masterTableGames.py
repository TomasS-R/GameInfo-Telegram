def createMasterTableGames(conn, tableName):

    columns = "id SERIAL PRIMARY KEY, game TEXT NOT NULL, url_game TEXT NOT NULL"

    try:
        cursor = conn.cursor()
        # Create table
        create_table_query = f"CREATE TABLE {tableName} ({columns});"
        cursor.execute(create_table_query)

        # Create policy
        enable_rls_query = f"ALTER TABLE {tableName} ENABLE ROW LEVEL SECURITY;"
        cursor.execute(enable_rls_query)

        # Create index
        create_index = f"CREATE INDEX idx_on_game ON {tableName} (game);"
        cursor.execute(create_index)

        # Insert data in table
        create_policy_insert = f"CREATE POLICY insert_policy ON {tableName} FOR INSERT TO authenticated WITH CHECK (true);"
        cursor.execute(create_policy_insert)

        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error creating table {tableName} and policy.", e)

def createPolicy(conn, tableName):
    try:
        cursor = conn.cursor()
        # Create policy
        enable_rls_query = f"ALTER TABLE {tableName} ENABLE ROW LEVEL SECURITY;"
        cursor.execute(enable_rls_query)

        # Insert data in table
        create_policy_insert = f"CREATE POLICY insert_policy ON {tableName} FOR INSERT TO authenticated WITH CHECK (true);"
        cursor.execute(create_policy_insert)

        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error creating policy {tableName}.", e)