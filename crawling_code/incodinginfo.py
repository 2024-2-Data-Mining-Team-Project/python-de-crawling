import chardet

file_path = '서울시 일반음식점 인허가 정보.csv'  # 파일 경로를 여기에 입력

# 파일을 바이너리 모드로 읽고 인코딩 탐지
with open(file_path, 'rb') as file:
    raw_data = file.read()  # 파일 내용을 모두 읽음
    result = chardet.detect(raw_data)  # 인코딩 탐지
    print(result)  # {'encoding': '추정된 인코딩', 'confidence': 신뢰도}

# 결과 예시: {'encoding': 'EUC-KR', 'confidence': 0.99}
