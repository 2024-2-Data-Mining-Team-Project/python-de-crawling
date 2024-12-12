import pandas as pd

file_paths = {
    "인구수": "C:/Users/김수현/DM project/인구수.csv",
    "개업률": "C:/Users/김수현/DM project/개업률.csv",
    "폐업률": "C:/Users/김수현/DM project/폐업률.csv",
    "점포수": "C:/Users/김수현/DM project/점포수.csv",
    "평균영업기간": "C:/Users/김수현/DM project/평균영업기간.csv",
    "신생기업_생존율_1년": "C:/Users/김수현/DM project/신생기업_생존율_1년.csv",
    "신생기업_생존율_3년": "C:/Users/김수현/DM project/신생기업_생존율_3년.csv",
    "신생기업_생존율_5년": "C:/Users/김수현/DM project/신생기업_생존율_5년.csv",
    "연차별_생존율_1년": "C:/Users/김수현/DM project/연차별_생존율_1년.csv",
    "연차별_생존율_3년": "C:/Users/김수현/DM project/연차별_생존율_3년.csv",
    "연차별_생존율_5년": "C:/Users/김수현/DM project/연차별_생존율_5년.csv",
    "임대시세": "C:/Users/김수현/DM project/임대시세.csv"
}

reference_file = pd.read_csv(file_paths["인구수"], encoding='cp949')
reference_order = reference_file['Unnamed: 0']

data_frames = {name: pd.read_csv(path, encoding='cp949') for name, path in file_paths.items()}

years = ['2018', '2019', '2020', '2021', '2022', '2023']

yearly_data = {year: pd.DataFrame() for year in years}

for year in years:
    year_dfs = []
    for name, df in data_frames.items():
        temp_df = df[['Unnamed: 0', year]].copy()
        temp_df.columns = ['지역', f'{name}']
        
        year_dfs.append(temp_df)

    yearly_data[year] = year_dfs[0]
    for temp_df in year_dfs[1:]:
        yearly_data[year] = yearly_data[year].merge(temp_df, on='지역', how='outer')

    yearly_data[year] = yearly_data[year].set_index('지역').loc[reference_order].reset_index()

for year, df in yearly_data.items():
    output_path = f"C:/Users/김수현/DM project/{year}.csv"
    df.to_csv(output_path, index=False, encoding='cp949')
    print(f"{output_path} 파일이 생성되었습니다.")