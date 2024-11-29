from geopy.geocoders import Nominatim
import pandas as pd
import postal.parser, postal.expand, postal.normalize

geolocator = Nominatim(
    domain="gc.ishkulov.site",
    user_agent="81xZiIp3PMWG",
    scheme="https"
)

# location = geolocator.geocode("Красная площадь, Москва")
# print(location.latitude, location.longitude)


# Загрузка CSV-файла в DataFrame
df = pd.read_csv('file.csv')

def clean_city_name(input_str):
    # Список возможных обозначений, которые нужно удалить
    to_remove = ['г', 'г.', 'город']
    words = input_str.split()
    cleaned = [word for word in words if word.lower() not in to_remove]
    return ' '.join(cleaned)

def clean_street_name(input_str):
    # Список сокращений для улиц
    to_remove = {'ул', 'ул.', 'улица', 'проспект', 'пр.', 'переулок', 'пер', 'пер.', 'шоссе', 'бульвар', 'бул.', 'тракт', 'пр-кт'}
    words = input_str.split()
    cleaned = [word for word in words if word.lower() not in to_remove]
    return ' '.join(cleaned)

def _geocode(query):
    location = geolocator.geocode(query, timeout=None)
    # print(query, '->', location)
    return query, location


def _parse_address(address):
    parsed = postal.parser.parse_address(
        address,
        # language='ru'
    )
    out = {}
    for v,k in parsed:
        if k == 'road':
            v = clean_street_name(v)

        if k == 'city':
            v = clean_city_name(v)
        
        if v:
            out[k] = v
        
    return out


def make_query(address):
    pa = _parse_address(address)
    # print(pa)
    
    city = pa.get('city', '')
    city = clean_city_name(city)
    street = pa.get('road', '')
    street = clean_street_name(street)

    query = {
        'city': city,
        'street': street
    }
    return query

# Итерация по строкам
count = 0
for index, row in df.iterrows():
    address = row[0]

    query = make_query(address)
    query, location = _geocode(query)

    if location:
        print(f"{address} | {query} | {location.latitude} | {location.longitude}")
        count += 1
    else:
        print(f"{address} | {query} | - | - ")

print(count)
