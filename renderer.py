import pandas as pd
import json

def renderer(criteria_c1, criteira_c2):

    print('renderer is working')
    # 讀取分析好的檔案

    file_path = '.\\stock_analyzer\\analyzed_result\\result.txt'

    with open(file_path, "r", encoding="utf-8") as f:
        result = json.load(f)


    # 拆解條件一的結果
    criteria_c1_result = []
    for stock_id in result:
        criteria_c1_result.append([
        stock_id,
        result[stock_id]['criteria_1']['條件一結果'],
        result[stock_id]['criteria_1'][criteria_c1['ROE']],
        result[stock_id]['criteria_1'][criteria_c1['EPS']]
        ])

    criteria_c1_result = pd.DataFrame(criteria_c1_result, columns=['Stock_id', 
                                                                 '條件一結果', 
                                                                 criteria_c1['ROE'], 
                                                                 criteria_c1['EPS']])

    # 拆解條件二的結果
    criteria_c2_result = []
    for stock_id in result:
        criteria_c2_result.append([
            stock_id,
            result[stock_id]['criteria_2']['條件二結果'],
            result[stock_id]['criteria_2'][criteira_c2['cashflow']],
            result[stock_id]['criteria_2'][criteira_c2['liabilities_TA']],
            result[stock_id]['criteria_2'][criteira_c2['liabilities_CP']],
            result[stock_id]['criteria_2'][criteira_c2['yeild']],
            result[stock_id]['criteria_2'][criteira_c2['yeild_AV']]
        ])
    criteria_c2_result = pd.DataFrame(criteria_c2_result, columns=['Stock_id', 
                                                                '條件二結果', 
                                                                criteira_c2['cashflow'], 
                                                                criteira_c2['liabilities_TA'],
                                                                criteira_c2['liabilities_CP'],
                                                                criteira_c2['yeild'],
                                                                criteira_c2['yeild_AV']])

    
    # 判斷條件一是否有啟用
    if criteria_c1_result['條件一結果'][0] == '無啟用': 
        print('**條件一沒有被啟用')
    else:
        # 統計有多少檔通過條件一
        pass_criteria_1 = criteria_c1_result.loc[criteria_c1_result['條件一結果'] == 'Pass']
        stock_pass_c1 = pass_criteria_1['Stock_id']
        print('通過條件一的公司: ', stock_pass_c1)
        print(f"**一共有{len(stock_pass_c1)}間公司通過條件一")

    
    # 判斷條件一是否有啟用
    if criteria_c1_result['條件一結果'][0] == '無啟用': 
        print("")
    # 判斷條件二是否有啟用
    elif criteria_c2_result['條件二結果'][0] == '無啟用':
        print('**條件二沒有被啟用')
    else:
        # 統計有多少檔通過條件一同時通過條件二
        pass_criteria_2 = criteria_c2_result.loc[criteria_c2_result['條件二結果'] == 'Pass']
        pass_c1_c2 = pass_criteria_2.loc[pass_criteria_2['Stock_id'].isin(stock_pass_c1)]
        stock_pass_c1_c2 = pass_c1_c2['Stock_id']

        print('通過條件一且通過條件二的公司: ', stock_pass_c1_c2)
        print(f"**一共有{len(stock_pass_c1_c2)}間公司同時通過條件一與條件二")
        stock_pass_c1_c2.to_csv('.\\stock_analyzer\\analyzed_result\\candidate.csv')

    # 判斷條件一是否有啟用
    if criteria_c1_result['條件一結果'][0] == '無啟用' or criteria_c2_result['條件二結果'][0] == '無啟用': 
        print('')
    else:
        # 多少檔通過條件一但無法通過條件二
        set_stock_pass_c1 = set(stock_pass_c1) # 轉換成 set 格式
        set_stock_pass_c1_c2 = set(stock_pass_c1_c2) # 轉換成 set 格式
        set_stock_pass_c1_not_c2 = set_stock_pass_c1 - set_stock_pass_c1_c2 # 使用 set 直接相減
        stock_pass_c1_not_c2 = list(set_stock_pass_c1_not_c2) # 轉換回陣列形式
        stock_pass_c1_not_c2 = pd.DataFrame(stock_pass_c1_not_c2) # 轉換回 Pandas 格式
        print('通過條件一但沒有通過條件二的公司: ', stock_pass_c1_not_c2)
        print(f"**一共有{len(stock_pass_c1_not_c2)}間公司通過條件一但沒有通過條件二")

    

