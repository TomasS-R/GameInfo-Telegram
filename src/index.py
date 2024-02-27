import logging, sys, time, config
import dataBaseFiles.createTableDynamic as dbf
import dataBaseFiles.databaseQuery as dbfdq
import dataBaseFiles.tablesDynamicsPlatforms as dbftdp
import dataBaseFiles.masterTableGames as dbftmg

logging.basicConfig(
    level = logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)

logger = logging.getLogger()

if (config.mode == "dev"):
    def run(updater):
        updater.start_polling()
        print("BOT CARGADO")
        updater.idle()
elif (config.mode == "prod"):
    def run(updater):
        updater.start_webhook(listen="0.0.0.0", port=config.PORT, url_path=config.TOKEN)
        updater.bot.set_webhook(f"https://{config.APP_NAME}.fly.dev/{config.TOKEN}")
        print("BOT CARGADO")
else:
    logger.info("No se especifico el MODE.")
    sys.exit()

# Create table and policy if not exists in supabase
def creatingTable(conn, tableName):
    if conn:
        # Table
        table = dbfdq.is_table_created(conn, tableName)
        if table == True:
            print(f"Table {tableName} already exists in Supabase.")
            time.sleep(2)
        else:
            print('Creating table and policy row level security (RLS)...')
            time.sleep(2)
            result = dbf.createTable(conn, tableName)
            if result == True:
                print(f"Table and RLS created!")
                return
        # Policy
        policy = dbfdq.is_policy_created(conn, tableName)
        if policy == True:
            print(f"Policy already exists in {tableName}.")
            time.sleep(2)
        else:
            print('Creating policy row level security (RLS)...')
            time.sleep(2)
            result = dbf.createPolicy(conn, tableName)
            if result == True:
                print(f"Policy RLS created!")
                return

def createTableGames(conn, tableName):
    if conn:
        for tableName in tableName:
            # Table
            table = dbfdq.is_table_created(conn, tableName)
            if table == True:
                print(f"Table {tableName} already exists in Supabase.")
            else: # Create table and policy RLS if not exists in supabase
                print(f'Creating table and policy row level security (RLS) for {tableName}...')
                if 'master_table_games' in tableName:
                    result = dbftmg.createMasterTableGames(conn, tableName)
                elif 'xbox_games' in tableName:
                    result = dbftdp.createTableXboxGames(conn, tableName)
                elif 'epic_games' in tableName:
                    result = dbftdp.createTableEpicGames(conn, tableName)
                if result == True:
                    print(f"Table and RLS created for {tableName}!")
            # Policy
            policy = dbfdq.is_policy_created(conn, tableName)
            if policy == True:
                print(f"Policy already exists in {tableName}.")
            else: # Create policy RLS if not exists in supabase
                print(f'Creating policy row level security (RLS) for {tableName}...')
                result = dbf.createPolicy(conn, tableName)
                if result == True:
                    print(f"Policy RLS for {tableName} created!")
                    return

creatingTable(config.connection, config.table_Name_Users)
createTableGames(config.connection, config.t_N_A_P)