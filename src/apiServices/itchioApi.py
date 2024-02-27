def eliminateStringsData(title):
    eliminate_strings = ["(steam)", "steam", "giveaway", "steam", "keys", "(itch.io)", "Giveaway", "Get ", " for ", "FREE!", "(GOG)"]
    for title_in_text in eliminate_strings:
        if title_in_text in title:
            title = title.replace(title_in_text,"")
        newtitle = title
    return newtitle

async def itchioApiPlatform(api_session) :
    data = []
    response = api_session.make_request("https://www.gamerpower.com/api/giveaways?platform=itchio")

    if response.status_code == 200:
        game_details = response.json()
        for game in game_details:
            if 'title' in game:
                name = game['title']
                title = eliminateStringsData(name)
            if 'image' in game:
                image = game['image']
            if 'worth' in game:
                price = game['worth']
            if 'type' in game:
                type = game['type']
            if 'end_date' in game and game['end_date'] != 'N/A':
                end_date = game['end_date']
            else:
                end_date = None
            if 'open_giveaway_url' in game:
                url = game['open_giveaway_url']
            
            data.append({'title': title, 'price': price, 'image_url': image, 'end_date': end_date, 'type': type, 'url_game': url})

    if data:
        print('------------------Itchio GAMES-----------------')
        for games in data:
            print('---GAME---')
            print(f"Titulo: {games['title']}\nPrecio: {games['price']}\nUrl Imagen: {games['image_url']} \nFecha fin: {games['end_date']}\nTipo: {games['type']}\nURL: {games['url_game']}")
        return data