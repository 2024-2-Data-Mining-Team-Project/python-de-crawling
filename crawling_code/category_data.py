import pandas as pd
import requests
import time

# 네이버 지도 API 설정
NAVER_CLIENT_ID = ""  
NAVER_CLIENT_SECRET = "" 

# 네이버 지도 API 호출 함수
def get_place_category_from_coordinates(x, y):
    """
    네이버 지도 API를 통해 좌표 정보를 검색하고 매장의 카테고리를 반환.
    """
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {
        "query": "카페",
        "x": x,
        "y": y,
        "display": 1,  # 한 번에 한 개의 결과만 요청
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 요청 실패 시 예외 발생
        result = response.json()
        if result["items"]:
            return result["items"][0]["category"]  # 첫 번째 결과의 카테고리 반환
        return None
    except requests.exceptions.RequestException as e:
        print(f"API 호출 실패: {e}")
        return None

# CSV 파일 읽기
file_path = '서울시 일반음식점 인허가 정보.csv'
data = pd.read_csv(file_path, on_bad_lines='skip', low_memory=False, encoding='utf-8')
print(f"CSV 파일 로드 성공: {file_path}")

# 사용할 업태구분명 리스트
categories = ["한식", "일식", "양식", "중식"]

# '경양식'을 '양식', '중국식'을 '중식'으로 변경
data['업태구분명'] = data['업태구분명'].replace({"경양식": "양식", "중국식": "중식"})

# '업태구분명'이 지정한 카테고리에 해당하는 데이터 필터링
filtered_data = data[data['업태구분명'].isin(categories)]

# '기타' 데이터만 필터링
misc_data = data[data['업태구분명'] == "기타"]

# '도로명주소'에서 '구' 정보 추출
filtered_data['구'] = filtered_data['도로명주소'].str.split().str[1]
misc_data['구'] = misc_data['도로명주소'].str.split().str[1]

# 좌표 정보를 사용해 네이버 지도 API로 카테고리 확인
cafe_counts_by_district = {}  # 구별 카페 매장 수 저장
save_interval = 100  # 매 100번째 처리마다 중간 저장
temp_output_file = '최종_중간_결과.csv'

print("기타 업태 매장에 대한 카페 수 계산을 시작합니다...")
for index, row in misc_data.iterrows():
    x = row['좌표정보(X)']
    y = row['좌표정보(Y)']
    district = row['구']
    if pd.notna(x) and pd.notna(y):  # 좌표 정보가 있는 경우만 처리
        category = get_place_category_from_coordinates(x, y)
        if category and "카페" in category:  # "카페"로 분류된 경우
            if district not in cafe_counts_by_district:
                cafe_counts_by_district[district] = 0
            cafe_counts_by_district[district] += 1
            print(f"{district}: 카페 매장 추가 - 총 {cafe_counts_by_district[district]}개")

    # 주기적으로 중간 저장
    if (index + 1) % save_interval == 0:
        print(f"중간 저장: {index + 1}번째까지 처리 완료")
        # 중간 결과 저장
        temp_output_rows = []
        for dist in filtered_data['구'].unique():
            row = {'구': dist}
            counts = filtered_data[filtered_data['구'] == dist]['업태구분명'].value_counts()
            for category in categories:
                row[category] = counts.get(category, 0)
            row["카페"] = cafe_counts_by_district.get(dist, 0)
            temp_output_rows.append(row)
        pd.DataFrame(temp_output_rows).to_csv(temp_output_file, index=False, encoding='utf-8-sig')

    # API 호출 간 간격 설정 (속도 제한 방지)
    time.sleep(0.1)  

# 최종 결과 저장
output_file = '최종_구별_카테고리_매장수.csv'
output_rows = []

for district in filtered_data['구'].unique():
    row = {'구': district}
    counts = filtered_data[filtered_data['구'] == district]['업태구분명'].value_counts()
    for category in categories:
        row[category] = counts.get(category, 0)
    row["카페"] = cafe_counts_by_district.get(district, 0)
    output_rows.append(row)

pd.DataFrame(output_rows).to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"CSV 파일이 성공적으로 생성되었습니다: {output_file}")
