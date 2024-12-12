import pandas as pd

file_path = '서울시정류소현황.csv'  
data = pd.read_csv(file_path, encoding='cp949')

stop_counts = data.groupby('행정구명')['정류소명'].nunique().reset_index(name='버스정류소')

order_file_path = '2023.csv'  
order_data = pd.read_csv(order_file_path, encoding='cp949')

desired_order = order_data['지역'].tolist()

stop_counts['행정구명'] = pd.Categorical(stop_counts['행정구명'], categories=desired_order, ordered=True)
sorted_stop_counts = stop_counts.sort_values('행정구명').reset_index(drop=True)

subway_file_path = '서울자치구별지하철역.CSV'  
subway_data = pd.read_csv(subway_file_path, encoding='cp949')

subway_data = subway_data.rename(columns={'자치구': '행정구명', '역개수': '지하철역'})

merged_data = sorted_stop_counts.merge(subway_data[['행정구명', '지하철역']], on='행정구명', how='left')

final_output_path = '서울시_자치구별_교통카운트.csv' 
merged_data.to_csv(final_output_path, index=False, encoding='cp949')

print(f"CSV 파일이 생성되었습니다: {final_output_path}")