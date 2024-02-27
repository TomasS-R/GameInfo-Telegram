def createTableXboxGames(conn, tableName):

    columns = "id SERIAL PRIMARY KEY, game_id INT NOT NULL, id_game_xbox INT8 NOT NULL, platforms TEXT[] NOT NULL, ea_play BOOLEAN[] NOT NULL, ubisoft_plus BOOLEAN[] NOT NULL, FOREIGN KEY (game_id) REFERENCES master_table_games(id)"

    try:
        cursor = conn.cursor()
        # Create table
        create_table_query = f"CREATE TABLE {tableName} ({columns});"
        cursor.execute(create_table_query)

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
        print(f"Error creating table {tableName} and policy.", e)

def createTableEpicGames(conn, tableName):

    columns = "id SERIAL PRIMARY KEY, game_id INT NOT NULL, type TEXT NOT NULL, image TEXT[] NOT NULL, price TEXT[] NOT NULL, date_start TIMESTAMPTZ NOT NULL, date_end TIMESTAMPTZ NOT NULL, FOREIGN KEY (game_id) REFERENCES master_table_games(id)"

    try:
        cursor = conn.cursor()
        # Create table
        create_table_query = f"CREATE TABLE {tableName} ({columns});"
        cursor.execute(create_table_query)

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