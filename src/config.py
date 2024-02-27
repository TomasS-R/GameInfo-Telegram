import logging, os, psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Telegram
TOKEN = os.getenv("TOKEN")
mode = os.getenv("MODE")

# Fly.io
PORT = int(os.environ.get("PORT", "8443"))
APP_NAME = os.environ.get("FLY_APP_NAME")

# Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
# Connection
supabase: Client = create_client(url, key)

# Postgres config
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")
database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")

# Table names
table_Name_Users = 'info_users'
# table_Names_Api_Platforms
t_N_A_P = ['master_table_games', 'xbox_games', 'epic_games']

def connect_database():
    try:
        conn = psycopg2.connect(user=database_user, password=database_password , dbname=database_name, host=database_host, port=database_port)
        if conn:
            logging.info("Conected to database.")
            return conn
        else:
            logging.info("Error to connected database.")
            return exit()
    except Exception as e:
        logging.info(f"Error to connected database.", e)
        return exit()

connection = connect_database()