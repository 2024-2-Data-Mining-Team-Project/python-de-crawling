import pandas as pd

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

# 제외할 도시 리스트
exclude_cities = ["고양시", "부천시", "성남시", "하남시"]

# 서울시 구만 남기고 다른 도시 제거
filtered_data = filtered_data[~filtered_data['구'].isin(exclude_cities)]

# 구별, 업태구분명별로 매장 수 세기
grouped_data = filtered_data.groupby(['구', '업태구분명']).size().unstack(fill_value=0)

# 결과를 CSV 파일로 저장
output_file = '카페제외_서울시_구별_업태별_매장수.csv'
grouped_data.to_csv(output_file, encoding='utf-8-sig')
print(f"CSV 파일이 생성되었습니다: {output_file}")
