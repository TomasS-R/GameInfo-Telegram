import asyncio
import aioschedule as scheduleAsync
import xboxGamePassGamesApi as xoga
import steamPoweredApi as spa
import epicGamesApi as epg
import gogApi as gpa
import itchioApi as itchapi
import humbleBundleApi as hba
from apiSessionsRequest import apiSession

class TaskRunnerProgrammed:
    def __init__(self, country_codes):
        self.country_codes = country_codes
        self.api_session = apiSession()

    async def programed_task_xbox_games(self):
        for country_code in self.country_codes:
            print(f'Running task xbox games for {country_code}...')
            await xoga.xboxObtainGamesApi(country_code, self.api_session)

    async def programed_task_steam_games(self):
        for country_code in self.country_codes:
            print(f'Running task Steam Powered for {country_code}...')
            await spa.steamPoweredApi(country_code, self.api_session)

    #async def programed_task_gog_games(self):
    #    await gpa.gogPlatformApi(self.api_session)

    #async def programed_task_itchio_games(self):
    #    await itchapi.itchioApiPlatform(self.api_session)
    
    async def programed_task_humbleBundle_games(self):
        await hba.storesApi(self.api_session)

    async def programed_task_epic_games(self):
        for country_code in self.country_codes:
            print(f'Rinning task epic games for {country_code}...')
            # The country code made be passed in mayus
            country_code = 'ar'
            final_country_code = country_code.upper()
            await epg.epicGamesApi(final_country_code, self.api_session)
    
    def close_session(self):
        self.api_session.close()

# Obtain country codes from DB
country_codes = ["ar"] #get_country_codes_from_db()

task_runner = TaskRunnerProgrammed(country_codes)

async def run_tasks_weekend():
    await task_runner.programed_task_xbox_games()
    await task_runner.programed_task_humbleBundle_games()

async def run_tasks_daily():
    await task_runner.programed_task_steam_games()
    await task_runner.programed_task_epic_games()
    #await task_runner.programed_task_gog_games()
    #await task_runner.programed_task_itchio_games()

scheduleAsync.every(20).seconds.do(run_tasks_daily)
scheduleAsync.every(30).seconds.do(run_tasks_weekend)

async def main_task():
    while True:
        await scheduleAsync.run_pending()
        await asyncio.sleep(1)
try:
    asyncio.run(main_task())
except KeyboardInterrupt:
    print('Exiting...')
    exit(0)
except Exception as e:
    print(f'Error: {e}')
    task_runner.close_session()
    exit(0)
finally:
    print(f'Cerrando sesion...')
    task_runner.close_session()