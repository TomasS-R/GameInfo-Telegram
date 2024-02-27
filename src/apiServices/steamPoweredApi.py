from fuzzywuzzy import fuzz
from itchioApi import eliminateStringsData

async def steamPoweredApi(country_code, api_session):
    game_models = []

    resp = api_session.make_request(f"https://store.steampowered.com/search/results/?force_infinite=1&maxprice=free&specials=1&json=1")

    if "items" in resp.text:
        items = resp.json()["items"]
        for item in items:
            name = item["name"]
            id_url = item["logo"]
            id = id_url.split("/")[5]
            link_game = f"https://store.steampowered.com/app/{id}"
            image = f"https://cdn.akamai.steamstatic.com/steam/apps/{id}/header.jpg"

            # Obtain more info of the game
            data_game = api_session.make_request(f"https://store.steampowered.com/api/appdetails?appids={id}&l=ES&cc={country_code}")
            extra_data_game = api_session.make_request(f"https://www.gamerpower.com/api/giveaways?platform=steam")

            if data_game.status_code == 200:
                game_details = data_game.json()
                if id in game_details:
                    game = game_details[id]
                    if 'data' in game:
                        data = game['data']
                        # Type of game/dlc
                        type = data['type']
                        # It's free?
                        is_free = data['is_free']
                    if 'price_overview' in data:
                        price_overview = data['price_overview']
                        if 'currency' in price_overview:
                            currency = price_overview['currency']
                        if 'initial_formatted' in price_overview:
                            price = price_overview['initial_formatted']
            if extra_data_game.status_code == 200:
                game_details = extra_data_game.json()
                for game in game_details:
                    if 'title' in game or item["name"] in game:
                        title = game['title'].lower()
                        name = name.lower()
                        end_date = "N/A"
                        # Delete some words that are not necessary and make the comparison more accurate
                        newtitle = eliminateStringsData(title)
                        similarity = fuzz.ratio(newtitle, name)
                        # If similarity is greater than 50% then the game is the same
                        if similarity > 80:
                            end_date = game['end_date']
        
        game_models.append({"title": name, "link":link_game, "image":image, 'type':type, 'currency':currency, 'price':price, 'end_date':end_date})

    if game_models:
        print('------------------STEAM GAME-----------------')
        for item in game_models:
            print('---GAME---')
            print(f"Titulo: {item['title']}\nTipo: {item['type']}\nPrecio: {item['currency']} {item['price']}\nImagen: {item['image']}\nUrl: {item['link']}\nEnd Date: {item['end_date']}")
    else:
        print("De momento no hay juegos")

    return game_models