import pandas as pd

# Load the uploaded files
area_data = pd.read_csv('면적.csv', encoding='utf-8')  # 한글 데이터 파일 읽기
category_data = pd.read_csv('최종_결과.csv', encoding='utf-8')  # 한글 데이터 파일 읽기

# Merge the two datasets on the matching region column
merged_data = pd.merge(category_data, area_data, left_on="구", right_on="지역").drop(columns=["지역"])

# Calculate density per unit area for each category
for category in ['한식', '일식', '양식', '중식', '카페']:
    merged_data[f'{category}_밀도'] = merged_data[category] / merged_data['면적']

# Drop original count columns and retain density columns for comparison
density_data = merged_data[['구'] + [f'{cat}_밀도' for cat in ['한식', '일식', '양식', '중식', '카페']]]

# Rename columns to English
density_data.rename(columns={
    '한식_밀도': 'Korean_Density',
    '일식_밀도': 'Japanese_Density',
    '양식_밀도': 'Western_Density',
    '중식_밀도': 'Chinese_Density',
    '카페_밀도': 'Cafe_Density'
}, inplace=True)

# Save the density data to a CSV file with proper encoding
output_path = 'Seoul_Food_Density.csv'
density_data.to_csv(output_path, index=False, encoding='utf-8-sig')  # 'utf-8-sig'로 저장하면 Excel에서 한글이 깨지지 않음

print("File saved at:", output_path)
