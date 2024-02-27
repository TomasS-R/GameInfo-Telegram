from itchioApi import eliminateStringsData

# Id_Games = https://gogapidocs.readthedocs.io/en/latest/gameslist.html?&format=0
# Api GOG: https://api.gog.com/products/{Id_Game}?expand=downloads,expanded_dlcs,description,screenshots,videos,related_products,changelog

async def gogPlatformApi(api_session):

    data = []

    resp = api_session.make_request(f"https://www.gamerpower.com/api/giveaways?platform=gog")

    if resp.status_code == 200:
        game_details = resp.json()
        for game in game_details:
            if 'title' in game:
                title = game['title']
                title = eliminateStringsData(title)
            if 'image' in game:
                image = game['image']
            if 'end_date' in game:
                end_date = game['end_date']
            if 'type' in game:
                type = game['type']
            if 'open_giveaway_url' in game:
                url = game['open_giveaway_url']
            if 'worth' in game:
                price = game['worth']
            data.append({'title': title, 'price': price, 'image_url': image, 'end_date': end_date, 'type': type, 'url_game': url})

    if data:
        print('------------------GOG GAMES-----------------')
        for games in data:
            print('---GAME---')
            print(f"Titulo: {games['title']}\nPrecio: {games['price']}\nUrl Imagen: {games['image_url']} \nFecha fin: {games['end_date']}\nTipo: {games['type']}\nURL: {games['url_game']}")
    
    return data

#gogPlatformApi()