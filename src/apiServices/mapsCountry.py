import requests, logging

def obtain_country(latitude, longitude):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
        
        response = requests.get(url)
        data = response.json()

        country = data.get('address', {}).get('country', 'Desconocido')
        country_code = data.get('address', {}).get('country_code', 'Desconocido')

        return country, country_code
    except Exception as e:
        print(f"Error to obtain country.", e)
