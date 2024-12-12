import requests
shops = {}
new_shop_survive_1y = {}
new_shop_survive_3y = {}
new_shop_survive_5y = {}
years_survive_1y = {}
years_survive_3y = {}
years_survive_5y = {}
avg_operate = {}
open_shop = {}
close_shop = {}
popluation = {}
rental = {}
def process(url_type, infoCategory, output, data_type) :
    url = f'https://golmok.seoul.go.kr/region/{url_type}.json'
    years = ['2018', '2019', '2020', '2021', '2022', '2023']
    for i in years:
        if i not in output:
            output[i] = {}  # 연도별 구 데이터를 저장할 서브 딕셔너리 생성
        
        payload = {
            'stdrYyCd': i,
            'stdrSlctQu': 'beforeQu',
            'stdrQuCd': 4,
            'stdrMnCd': i + "12",
            'selectTerm': 'quarter',
            'svcIndutyCdL': 'CS100000',
            'svcIndutyCdM': 'all',
            'stdrSigngu': '11',
            'selectInduty': '1',
            'infoCategory': infoCategory
        }
        
        # API 요청
        response = requests.post(url, data=payload)
        result = response.json()
        
        # gu_process 함수로 필요한 구 데이터를 추출
        gu_dict = gu_process(result, data_type)
        output[i] = gu_dict
    return output
def gu_process(result, data_type) :
    gu_dict = {}
    for i in result :
        if i['GUBUN'] == "gu" :
            if len(data_type) == 1 :
                gu_dict[i['NM']] = i[data_type[0]]
            else :
                for j in data_type :
                    try :
                        gu_dict[i['NM']] += float(i[j])
                    except :
                        gu_dict[i['NM']] = float(i[j])
                    
    return gu_dict

process_methods = [
    ['selectStoreCount', 'store', shops, ['THIRD_TOT']], # 전체 점포수
    ['selectSurvivalRate', 'survival', new_shop_survive_1y, ['THIRD_1Y']], # 1년생존율
    ['selectSurvivalRate', 'survival', new_shop_survive_3y, ['THIRD_3Y']], # 3년생존율
    ['selectSurvivalRate', 'survival', new_shop_survive_5y, ['THIRD_5Y']], # 5년생존율
    ['selectSurvivalRate2', 'survival2', years_survive_1y, ['THIRD_1Y']], # 1년생존율
    ['selectSurvivalRate2', 'survival2', years_survive_3y, ['THIRD_3Y']], # 3년생존율
    ['selectSurvivalRate2', 'survival2', years_survive_5y, ['THIRD_5Y']], # 5년생존율
    ['selectSurvivalAvg', 'operatingPeriod', avg_operate, ['FIRSTAVG']], # 최근 10년기준
    ['selectOpening', 'opening', open_shop, ['OPBIZ_STOR_CO_3']], # 개업수
    ['selectOpening', 'opening', close_shop, ['CLSBIZ_STOR_CO_3']], # 폐업수
    ['selectPopulation', 'population', popluation, ['TOT_FLPOP_CO_3', 'TOT_REPOP_CO_3', 'TOT_WRC_POPLTN_CO_3']], # 인구수 - 길단위 유동인구 + 주거인구 + 직장인구
    ['selectRentalPrice', 'rent', rental, ['BF3_TOT_FLOOR']] # 임대료 - 전체데이터


]
for i in process_methods :
    print(process(i[0], i[1], i[2], i[3]))
import pandas as pd
output_datas = {'shops' : "점포수.csv",
                'new_shop_survive_1y' : '신생기업_생존율_1년.csv',
                'new_shop_survive_3y' : '신생기업_생존율_3년.csv',
                'new_shop_survive_5y' : '신생기업_생존율_5년.csv',
                'years_survive_1y' : '연차별_생존율_1년.csv',
                'years_survive_3y' : '연차별_생존율_3년.csv',
                'years_survive_5y' : '연차별_생존율_5년.csv',
                'avg_operate' : '평균영업기간.csv',
                'open_shop' : '개업률.csv',
                'close_shop' : '폐업률.csv',
                'popluation' : '인구수.csv',
                'rental' : '임대시세.csv'}
pd.DataFrame(shops).to_csv(output_datas['shops'], encoding='cp949')
pd.DataFrame(new_shop_survive_1y).to_csv(output_datas['new_shop_survive_1y'], encoding='cp949')
pd.DataFrame(new_shop_survive_3y).to_csv(output_datas['new_shop_survive_3y'], encoding='cp949')
pd.DataFrame(new_shop_survive_5y).to_csv(output_datas['new_shop_survive_5y'], encoding='cp949')
pd.DataFrame(years_survive_1y).to_csv(output_datas['years_survive_1y'], encoding='cp949')
pd.DataFrame(years_survive_3y).to_csv(output_datas['years_survive_5y'], encoding='cp949')
pd.DataFrame(years_survive_5y).to_csv(output_datas['years_survive_3y'], encoding='cp949')
pd.DataFrame(avg_operate).to_csv(output_datas['avg_operate'], encoding='cp949')
pd.DataFrame(open_shop).to_csv(output_datas['open_shop'], encoding='cp949')
pd.DataFrame(close_shop).to_csv(output_datas['close_shop'], encoding='cp949')
pd.DataFrame(popluation).to_csv(output_datas['popluation'], encoding='cp949')
pd.DataFrame(rental).to_csv(output_datas['rental'], encoding='cp949')