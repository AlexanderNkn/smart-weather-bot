import json

with open('bot/assets/city.list.min.json', encoding='utf-8') as f:
    CITIES = json.load(f)


def find_city(query):
    result = []
    for city in CITIES:
        city_name = city['name'].lower()
        if query.lower() == city_name:
            result.insert(0, city)
        elif query.lower() in city_name:
            result.append(city)
    return result


def find_city_by_coords(longitude, latitude):
    result = []
    for city in CITIES:
        longitude_diff = abs(longitude - city['coord']['lon'])
        latitude_diff = abs(latitude - city['coord']['lat'])
        if longitude_diff <= 1 and latitude_diff <= 1:
            result.append((city, longitude_diff + latitude_diff))
    result = sorted(result, key=lambda c: c[1])
    return [c[0] for c in result]