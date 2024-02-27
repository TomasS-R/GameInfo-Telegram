import logging
from config import supabase

def is_table_created(conn, table_name):
    try:
        cursor = conn.cursor()
        table_name_lower = table_name.lower()
        cursor.execute(f"SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = '{table_name_lower}');")
        result = cursor.fetchone()
        cursor.close()
        return result[0] == True
    except Exception as e:
        print(f"Error to verify the table {table_name}.", e)
        return False

def is_policy_created(conn, table_name):
    try:
        cursor = conn.cursor()
        table_name_lower = table_name.lower()
        cursor.execute(f"SELECT relrowsecurity FROM pg_class WHERE relname = '{table_name_lower}'")
        result = cursor.fetchone()
        cursor.close()
        return result[0] == True
    except Exception as e:
        print(f"Error to verify the policy {table_name}.", e)
        return False

# Save the link in the database from the user who requested it
def saveData(tableName, user_name_Tg, user_id_tg, country, country_code, date, platforms, start_question):
    try:
        response = supabase.table(tableName).insert({"user_name_tg": user_name_Tg, "country": country, "country_code": country_code, "user_id_tg": user_id_tg, "date": date, "platforms": platforms, "start_question": start_question}).execute()
    except Exception as e:
        print(f"Error to save data in table {tableName}.", e)
        return False
    return bool(response.data)

# Corroborate state of start_question column
def selectStartQuestion(tableName, user_id_tg, position):
    try:
        current_data = supabase.table(tableName).select("start_question").eq("user_id_tg", user_id_tg).execute()
        return current_data.data[position]['start_question']
    except Exception as e:
        print(f"Error to select data in table {tableName}.", e)
        return False

# Update start_question column
def updateStartQuestion(tableName, user_id_tg, start_question):
    try:
        current_array = selectStartQuestion(tableName, user_id_tg, 0)
        if current_array:
            current_array[0] = start_question
        else:
            current_array = [start_question]

        response = supabase.table(tableName).update({"start_question": current_array}).eq("user_id_tg", user_id_tg).execute()
    except Exception as e:
        print(f"Error to update data in table {tableName}.", e)
        return False
    return bool(response.data)

# Select user if in the database
def selectUser(tableName, user_id_tg):
    try:
        current_data = supabase.table(tableName).select("*").eq("user_id_tg", user_id_tg).execute()
        
        if current_data.data:
            return True
        return False
    except Exception as e:
        print(f"Error to select data user in table {tableName}.", e)
        return False

# Select country if exists in the database
def selectCountry(tableName, user_id_tg):
    try:
        current_data = supabase.table(tableName).select("country").eq("user_id_tg", user_id_tg).execute()
        if current_data.data and current_data.data[0]['country'] is None:
            return False
        return True
    except Exception as e:
        print(f"Error to select country in the user in table {tableName}.", e)
        return False

# Save country in the database
def saveCountry(tableName, user_id_tg, country, country_code):
    try:
        response = supabase.table(tableName).update({"country": country, "country_code": country_code}).eq("user_id_tg", user_id_tg).execute()
    except Exception as e:
        print(f"Error to save country in the user in table {tableName}.", e)
        return False
    return bool(response.data)

# Select platforms if exists in the database
def selectPlatforms(tableName, user_id_tg):
    try:
        current_data = supabase.table(tableName).select("platforms").eq("user_id_tg", user_id_tg).execute()
        if current_data.data and current_data.data[0]['platforms'] is None:
            return False
        return True
    except Exception as e:
        print(f"Error to select platforms in the user in table {tableName}.", e)
        return False

# Save platforms in the database
def savePlatforms(tableName, user_id_tg, platforms):
    try:
        response = supabase.table(tableName).update({"platforms": platforms}).eq("user_id_tg", user_id_tg).execute()
    except Exception as e:
        print(f"Error to save platforms in the user in table {tableName}.", e)
        return False
    return bool(response.data)