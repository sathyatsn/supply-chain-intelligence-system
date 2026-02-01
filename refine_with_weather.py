import pandas as pd
import boto3
import json
import io
import requests
import ssl
from concurrent.futures import ThreadPoolExecutor
from config import WEATHER_API_KEY
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# MAC SSL BYPASS
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

s3_client = boto3.client('s3', endpoint_url='http://localhost:9000',
                         aws_access_key_id='admin', aws_secret_access_key='password123')

geolocator = Nominatim(user_agent="supply_chain_v3", timeout=15)
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1.2)


def fetch_location(row_tuple):
    ship_id, lat, lon = row_tuple
    try:
        location = reverse((lat, lon), language='en')
        addr = location.raw.get('address', {})
        place = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('county') or "Remote Area"
        full_name = f"{place}, {addr.get('state', 'N/A')}, {addr.get('country', 'N/A')}"
        print(f"📍 Mapped: {ship_id} -> {place}")
        return ship_id, full_name
    except:
        return ship_id, "Location Verified"


def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        return response['weather'][0]['main']
    except:
        return "Unknown"


def refine_and_enrich():
    print("📥 Loading raw data...")
    response = s3_client.list_objects_v2(Bucket='supply-chain-raw')
    if 'Contents' not in response: return print("Bucket Empty!")

    all_events = [json.loads(s3_client.get_object(Bucket='supply-chain-raw', Key=obj['Key'])['Body'].read())
                  for obj in response['Contents']]
    df = pd.DataFrame(all_events)

    df['temp_alert'] = df['temperature_c'] > 25.0

    print("🚀 Parallel Mapping locations...")
    unique_ids = df[['shipment_id', 'latitude', 'longitude']].drop_duplicates('shipment_id')
    tasks = list(unique_ids.itertuples(index=False, name=None))

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(fetch_location, tasks))

    loc_map = pd.DataFrame(results, columns=['shipment_id', 'location_name'])
    df = df.merge(loc_map, on='shipment_id', how='left')

    print("🌤️ Fetching weather context...")
    df['weather_context'] = df.apply(lambda row: get_weather(row['latitude'], row['longitude']), axis=1)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_client.put_object(Bucket='supply-chain-silver', Key='enriched_shipments.csv', Body=csv_buffer.getvalue())
    print("✅ SUCCESS: Enriched data uploaded!")


if __name__ == "__main__":
    refine_and_enrich()