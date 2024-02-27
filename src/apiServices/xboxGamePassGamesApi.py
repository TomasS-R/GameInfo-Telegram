from datetime import datetime
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to obtain the games from the Xbox Game Pass API and all necesarie data
def fetch_url(ID, country_code, api_session):
    if country_code == None or country_code == '':
        country_code = 'us'
    URL = f'https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={ID}&market={country_code}&languages=es-es&MS-CV=DGU1mcuYo0WMMp'
    response_URL = api_session.make_request(URL)
    webDataGame = response_URL.json()
    for game in webDataGame['Products']:
        # Obtain the title of the game
        for localized_property in game['LocalizedProperties']:
            gameTitle = localized_property['ProductTitle']
            gameShortTitle = localized_property['ShortTitle']
            gameSortTitle = localized_property['SortTitle']
            if gameShortTitle == None or gameShortTitle == '':
                gameShortTitle = gameTitle
            if gameTitle == None or gameTitle == '':
                gameShortTitle = gameSortTitle
        # Obtain the release date of the game
        for market_property in game['MarketProperties']:
            date_string = market_property['OriginalReleaseDate']
            date_string = date_string[:-9] + date_string[-1]
            date_string = date_string.split("T")[0]
            date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
            date = date_object.strftime("%d/%m/%Y")
        # Identify if the game is available in EA Play or ubisoft+
        EAPlay = False
        Ubisoft_plus = False
        for localized_property in game['LocalizedProperties']:
            if 'EligibilityProperties' in localized_property:
                EligibilityProperties = localized_property['EligibilityProperties']
                if 'Remediations' in EligibilityProperties:
                    for remediation in EligibilityProperties['Remediations']:
                        if remediation['Description'] == 'Better With EA Play':
                            EAPlay = True
                        elif remediation['Description'] == 'play more great games with Ubisoft+.':
                            Ubisoft_plus = True
                            break
        # Obtain the platforms where the game is available
        for displaySkuAvailability in game['DisplaySkuAvailabilities']:
            #dayingamepassadded = "N/A"
            for availability in displaySkuAvailability['Availabilities']:
                conditions = availability['Conditions']
                if 'ClientConditions' in conditions:
                    client_conditions = conditions['ClientConditions']
                    if 'AllowedPlatforms' in client_conditions:
                        allowed_platforms = client_conditions['AllowedPlatforms']
                        PlatformGame = []
                        xbox_added = False
                        if len(allowed_platforms) > 1:
                            for platform in allowed_platforms:
                                PlatformName = platform['PlatformName']
                                if PlatformName == 'Windows.Desktop':                                
                                    PlatformNameGame = 'PC'
                                    PlatformGame.append(PlatformNameGame)
                                elif (PlatformName == 'Windows.Xbox' or PlatformName == 'Windows.Core') and not xbox_added:
                                    PlatformNameGame = 'Xbox Console'
                                    PlatformGame.append(PlatformNameGame)
                                    xbox_added = True
                        else:
                            for platform in allowed_platforms:
                                PlatformName = platform['PlatformName']
                                if PlatformName == 'Windows.Desktop':                                
                                    PlatformNameGame = 'PC'
                                elif PlatformName == 'Windows.Xbox':
                                    PlatformNameGame = 'Xbox Console'
                                else:
                                    PlatformNameGame = 'Otro'
                                PlatformGame.append(PlatformNameGame)
                        #break
                    #break
                if 'StartDate' in conditions:
                    dayInGamePassAdded = conditions['StartDate']
                    date_iso = dayInGamePassAdded.rstrip('Z')
                    date_iso = date_iso[:-2] + date_iso[-1]
                    date_iso_datetime = datetime.strptime(date_iso, "%Y-%m-%dT%H:%M:%S.%f")
                    dayInGamePassAdded = date_iso_datetime.strftime("%d/%m/%Y")
            type = "Game"
            if 'Sku' in displaySkuAvailability:
                sku = displaySkuAvailability['Sku']
                if 'Properties' in sku:
                    properties = sku['Properties']
                    if "Packages" in properties:
                        packages = properties['Packages']
                        for package in packages: 
                            if 'MainPackageFamilyNameForDlc' in package:
                                MainPackageFamilyNameForDlc = package['MainPackageFamilyNameForDlc']
                                if MainPackageFamilyNameForDlc is not None:
                                    type = "DLC"
                                """if MainPackageFamilyNameForDlc != "null":
                                    type = MainPackageFamilyNameForDlc"""
    return gameShortTitle, ID, date, PlatformGame, EAPlay, Ubisoft_plus, type, dayInGamePassAdded

async def xboxObtainGamesApi(country_code, api_session):
    if country_code == None or country_code == '':
        country_code = 'us'
    game_ids = set()
    count = 0
    id_list = [
                '29a81209-df6f-41fd-a528-2ae6b91f719c', # All games xbox game pass
               'fdd9e2a7-0fee-49f6-ad69-4354098401ff', # PC games xbox game pass
               'f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e', # All Console games xbox game pass
               'b8900d09-a491-44cc-916e-32b5acae621b'  # All EA Play games xbox game pass
              ]
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for game_id in id_list:
            URL_ID_DATA = f'https://catalog.gamepass.com/sigls/v2?id={game_id}&language=en-es&market={country_code}'
            response_ID = api_session.make_request(URL_ID_DATA)
            ID_GameXbox = response_ID.json()
            for game in ID_GameXbox:
                if "id" in game and game['id'] not in game_ids:
                    ID = game['id']
                    game_ids.add(ID)
                    futures.append(executor.submit(fetch_url, ID, country_code, api_session))
        for future in as_completed(futures):
            count += 1
            gameShortTitle, ID, date, PlatformName, EAPlay, Ubisoft_plus, type, addedInGamePass = future.result()
            game_url_format = gameShortTitle.replace(" ", "")
            Url = f'https://www.xbox.com/es-{country_code}/games/store/{game_url_format}/{ID}'
            Url_Game = quote(Url, safe=':/')
            print(count, 'Titulo: '+gameShortTitle+' ID: '+ID+' Lanzado el: '+date+' Url Game: '+Url_Game+' Plataforma: '+', '.join(PlatformName)+' EA Play: '+str(EAPlay)+' Ubisoft+: '+str(Ubisoft_plus)+' Tipo: '+type+ ' Agregado al game pass el: '+addedInGamePass)
    print('Total de juegos:',count)