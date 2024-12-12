import pandas as pd

# CSV 파일 경로
file_path = '최종_결과.csv'

# 데이터를 UTF-8로 읽어오기 (파일의 원래 인코딩이 utf-8인 경우)
data = pd.read_csv(file_path, encoding='utf-8')

# 카테고리 컬럼 선택 (첫 번째 컬럼 '구' 제외)
categories = data.columns[1:]

# 각 카테고리별 총합 계산
category_totals = data[categories].sum()

# 비율 계산 및 새로운 데이터프레임 생성
percentage_df = data.copy()
for category in categories:
    # 각 구의 카테고리 비율 계산
    percentage_df[category] = (data[category] / category_totals[category]) * 100

# 새로운 CSV 파일로 저장 (UTF-8-SIG 인코딩 사용)
output_file_path = 'Proportion_Of_Categories_By_Region.csv'
percentage_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"CSV 파일이 '{output_file_path}' 경로에 UTF-8-SIG 인코딩으로 저장되었습니다.")
