from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

# Stores: https://www.cheapshark.com/api/1.0/stores

def transformTitleGameUrl(gameTitle, storeName):
    titleUrl = gameTitle.translate(str.maketrans(':-\!?-()','        ')).replace(' ', '-')
    titleUrl = titleUrl.translate(str.maketrans('', '', ",'."))
    if storeName == 'Fanatical':
        titleUrl = titleUrl.replace('-bundle', '')
    return titleUrl

def humbleChoice_data(api_session):

    gameChoiseCollect = []

    humbleChoise = api_session.make_request(f"https://dangarbri.tech/humblechoice/")
    now = datetime.now()
    current_month = now.strftime("%B-%Y").lower()
    if humbleChoise.status_code == 200:
        soupChoise = BeautifulSoup(humbleChoise.text, 'html.parser')
        gamesChoice = soupChoise.find_all('h2', {'id': current_month})
        for element in gamesChoice:
            if element:
                ul = element.find_next_sibling('ul')
                if ul:
                    for li in ul.find_all('li'):
                        a = li.find('a')
                        if a:
                            name = li.text
                            linkNoFormated = a['href']
                            link = linkNoFormated.replace('?partner=dangarbri', '?partner=gamerex')
                            gameChoiseCollect.append({'name': name, 'link': link})
    else:
        print("Error")
    if gameChoiseCollect:
        return gameChoiseCollect


async def storesApi(api_session):

    games_by_platform = []

    info = api_session.make_request("https://www.cheapshark.com/api/1.0/stores")

    # Obtain games of humble choice
    dataHumble = humbleChoice_data(api_session)

    if info.status_code == 200:
        result = info.json()
        platforms = ['Humble Store', 'GamersGate', 'Fanatical']
        for stores in result:
            if stores['storeName'] in platforms:
                storeID = stores['storeID']
                store_Data = api_session.make_request(f"https://www.cheapshark.com/api/1.0/deals?storeID={storeID}")

                if store_Data.status_code == 200:
                    store_result = store_Data.json()
                    for game in store_result:
                        if game['salePrice'] == '0.00' :
                            gameTitle = game['title']
                            imageUrl = game['thumb']
                            normalPrice = game['normalPrice']
                            salePrice = game['salePrice']
                            metacriticLink = game['metacriticLink']
                            nameStore = stores['storeName']
                            if nameStore == 'GamersGate':
                                parsed_url = urlparse(imageUrl)
                                segments = parsed_url.path.split('/')
                                titleUrl = segments[-2]
                                if titleUrl.isdigit():
                                    titleUrl = transformTitleGameUrl(gameTitle, nameStore)
                                url = "https://www.gamersgate.com/product/"+titleUrl
                            elif nameStore == 'Humble Store':
                                title = game['title'].lower()
                                game = transformTitleGameUrl(title, nameStore)
                                url = "https://www.humblebundle.com/store/"+game
                                while '--' in url:
                                    url = url.rstrip('-')
                                    url = url.replace('--', '-')
                            elif nameStore == 'Fanatical':
                                if isinstance(metacriticLink, str):
                                    parsed_url = urlparse(metacriticLink)
                                    segments = parsed_url.path.split('/')
                                    segments = [segment for segment in segments if segment]
                                    desired_segment = segments[-1]
                                    url = "https://www.fanatical.com/en/game/"+desired_segment
                                else:
                                    title = game['title'].lower()
                                    game = transformTitleGameUrl(title, nameStore)
                                    url = "https://www.fanatical.com/en/game/"+game
                                    while '--' in url:
                                        url = url.rstrip('-')
                                        url = url.replace('--', '-')
                            else:
                                url = None
                            games_by_platform.append({'platform': stores['storeName'], 'game': gameTitle, 'link': url, 'image': imageUrl, 'price': salePrice})
    if games_by_platform or dataHumble:
        if games_by_platform:
            print('------------------ GAMES -----------------')
            last_platform = None
            for game_info in games_by_platform:
                    if game_info['platform'] != last_platform:
                        print(f"--- {game_info['platform']} ---")
                        last_platform = game_info['platform']
                    print("--- Game ---")
                    print(f"Juego: {game_info['game']}\nUrl: {game_info['link']}\nImagen: {game_info['image']}\nPrecio: {game_info['price']}")
        if dataHumble:
            print('------------------ Humble Choice -----------------')
            for games in dataHumble:
                print(f"Juego: {games['name']}")
                print(f"Enlace: {games['link']}")
    else:
        print(f"No hay juegos")