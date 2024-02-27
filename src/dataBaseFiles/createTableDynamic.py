def createTable(conn, tableName):

    columns = {
        'id SERIAL PRIMARY KEY,'
        'user_name_Tg TEXT NOT NULL,'
        'user_id_tg INT8 NOT NULL,'
        'date TIMESTAMPTZ NOT NULL,'
        'start_question BOOLEAN[] NOT NULL,'
        'country TEXT NULL,'
        'country_code TEXT NULL,'
        'platforms TEXT[] NULL'
    }

    columns_str = ", ".join(columns)

    try:
        cursor = conn.cursor()
        # Create table
        create_table_query = f"CREATE TABLE {tableName} ({columns_str});"
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