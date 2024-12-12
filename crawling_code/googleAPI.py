import requests
import json
import mpu
import time
import time
from tqdm import tqdm
import os
from mpu import haversine_distance
import pandas as pd
from collections import defaultdict

def getresultlist(api_key, location, radius, keywordlist):
    results = []
    for keyword in keywordlist:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={keyword}&key={api_key}'
        
        while True:
            request = requests.get(url)
            js = json.loads(request.text)
            results.extend(js['results'])

            next_page_token = js.get('next_page_token')
            if not next_page_token:
                break
            url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}'
            time.sleep(2)  
    return results


def get_market(latloc, lngloc, api_key):
    location = f"{latloc},{lngloc}"
    radius = "500"  
    results = getresultlist(api_key, location, radius, ['restaurant', 'cafe', 'bakery', 'dining'])

    market_data = []
    nameset = set()
    for result in results:
        name = result['name']
        lat1 = result['geometry']['location']['lat']
        lng1 = result['geometry']['location']['lng']
        address = result.get('vicinity', '')

        # 서울에 위치한 것만
        if "서울" in address and name not in nameset:
            nameset.add(name)
            distance = "{:0.2f}".format(mpu.haversine_distance((latloc, lngloc), (lat1, lng1)))
            market_data.append({
                '음식점 이름': name,
                '거리(km)': distance,
                '위도': lat1,
                '경도': lng1,
                '주소': address
            })

    return market_data

def merge_data(bus_df, subway_df):
    if os.path.exists("서울_지하철역_근접_버스정류장.xlsx"):
        output_data = pd.read_excel("서울_지하철역_근접_버스정류장.xlsx")
        return output_data

    output_data = []
    for _, subway_row in tqdm(subway_df.iterrows(), total=subway_df.shape[0], desc="지하철역 처리 중"):
        subway_name = subway_row['이름']
        subway_location = (subway_row['위도'], subway_row['경도'])
        nearby_buses = []

        for _, bus_row in bus_df.iterrows():
            bus_location = (bus_row['위도'], bus_row['경도'])
            distance = haversine_distance(subway_location, bus_location)
            if distance <= 0.5:
                nearby_buses.append(bus_row['이름'])

        output_data.append({
            "지하철역 이름": subway_name,
            "버스 정류장 수": len(nearby_buses),
            "근접 버스 정류장 목록": ", ".join(nearby_buses)
        })

    output_df = pd.DataFrame(output_data)
    output_df.to_excel("서울_지하철역_근접_버스정류장.xlsx", index=False)
    return output_df

def find_coordinates(station_name, subway_df):
    row = subway_df[subway_df['이름'] == station_name]
    if not row.empty:
        return row.iloc[0]['위도'], row.iloc[0]['경도']
    else:
        return None, None

seoul_bus = pd.read_excel("서울시버스정류소위치정보(20241002).xlsx")
seoul_subway = pd.read_csv("지하철역_좌표.csv", encoding='cp949')

bus_df = seoul_bus[['정류소명', 'X좌표', 'Y좌표']].copy()
bus_df = bus_df.rename(columns={'정류소명': '이름', 'X좌표': '경도', 'Y좌표': '위도'})
bus_df['종류'] = '버스 정류소'

subway_df = seoul_subway[['역이름', 'x', 'y']].copy()
subway_df = subway_df.rename(columns={'역이름': '이름', 'x': '경도', 'y': '위도'})
subway_df['종류'] = '지하철역'

combined_df = merge_data(bus_df, subway_df)
print(len(combined_df))

restaurant_counts = defaultdict(lambda: {'버스 정류소': 0, '지하철역': 0})

api_key = "AIzaSyCvd2WmFcS5vzt5Irlr-YI66pbwJyzl00c"
count = 0
total = len(combined_df)

for _, row in tqdm(combined_df.iterrows(), total=len(combined_df), desc="음식점 데이터 처리 중"):
    lat, lng = find_coordinates(row['지하철역 이름'], subway_df)
    if lat is None or lng is None:
        continue
    market_data = get_market(lat, lng, api_key)
    
    for market in market_data:
        restaurant_name = market['음식점 이름']
        restaurant_counts[restaurant_name]['지하철역'] += 1
        restaurant_counts[restaurant_name]['버스 정류소'] = row['버스 정류장 수']
        restaurant_counts[restaurant_name]['위도'] = market['위도']
        restaurant_counts[restaurant_name]['경도'] = market['경도']

output_data = []
for name, counts in restaurant_counts.items():
    output_data.append({
        "음식점 이름": name,
        "위도": counts['위도'],
        "경도": counts['경도'],
        "버스 정류소 수": counts['버스 정류소'],
        "지하철역 수": counts['지하철역']
    })

output_df = pd.DataFrame(output_data)
output_df.to_excel("서울_정류소_음식점_카운트2.xlsx", index=False)

print("파일이 성공적으로 저장되었습니다: 서울_정류소_음식점_카운트2.xlsx")
