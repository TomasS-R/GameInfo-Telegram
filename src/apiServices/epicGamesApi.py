# normal_Url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
# URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=ES&allowCountries=ES"
async def epicGamesApi(country_code, api_session):
    URL = f"https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-{country_code}&country={country_code}&allowCountries={country_code}"
    response = api_session.make_request(URL)

    response_data = response.json()

    storeElements = response_data['data']['Catalog']['searchStore']['elements']

    data = []
    for element in storeElements:
        title = element['title']
        description = element['description']
        offerType = element['offerType']
        # Thumbnail
        thumbnail = element['keyImages']
        # Url
        Url_Direction = element['catalogNs']['mappings']
        # Price
        price = element['price']['totalPrice']['fmtPrice']['originalPrice']
        # PromotionsOffers obtain date start and date end promotion
        if element['promotions'] is not None:
            PromotionsOffers = element['promotions']['promotionalOffers']
            upcomingPromotionalOffers = element['promotions']['upcomingPromotionalOffers']
        dateStart = None
        dateEnd = None

        for thumbnail in thumbnail:
            if (thumbnail['type'] == 'OfferImageWide'):
                thumbnail = thumbnail['url']
                break
        
        for Url_Direction in Url_Direction:
            if Url_Direction['pageSlug']:
                Slug = Url_Direction['pageSlug']
                Url_Direction = f"https://www.epicgames.com/store/es-ES/p/"+Slug
                break
        
        if PromotionsOffers:
            for calendar in PromotionsOffers:
                for date in calendar['promotionalOffers']:
                    dateStart = date['startDate']
                    dateEnd = date['endDate']
                break
        else:
            for calendar in upcomingPromotionalOffers:
                for date in calendar['promotionalOffers']:
                    dateStart = date['startDate']
                    dateEnd = date['endDate']
                break
        
        if offerType == 'BASE_GAME':
            offerType = 'Game'
        elif offerType == 'DLC':
            offerType = 'DLC'
        else:
            offerType = 'Otro'

        data.append({ 'title': title, 'description':description, 'offerType':offerType, 'thumbnail':thumbnail, 'urlSlug':Url_Direction, 'price':price, 'dateStart':dateStart, 'dateEnd':dateEnd})

    if data:
        print('------------------EPIC GAMES-----------------')
        for item in data:
            print('---GAME---')
            print(f"Titulo: {item['title']}\nDescripcion: {item['description']}\nTipo: {item['offerType']}\nURL: {item['urlSlug']}\nImagen: {item['thumbnail']} \nPrecio: {item['price']}\nFecha de inicio: {item['dateStart']}\nFecha de fin: {item['dateEnd']}")
    
    return data