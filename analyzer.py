import pandas as pd
import math
# 主要驅動程式
def analyzer(file_path, search_criteria):

    print('analyzer is working')
    
    #讀取檔案
        # 由於有可能出現公司沒有資產負債表的狀況，所以要做一個 try 的動作
    fake_bs_file_path = ".\\stock_analyzer\\stock_data\\fake_bs.csv"
    try:   
        bs = pd.read_csv(file_path['bs_file_path']) #讀取真資產負債表
    except:
        bs = pd.read_csv(fake_bs_file_path) #讀取假資負債表


        # 由於有可能出現公司沒有損益表的狀況，所以要做一個 try 的動作
    fake_fs_file_path = ".\\stock_analyzer\\stock_data\\fake_fs.csv"
    try: 
        fs = pd.read_csv(file_path['fs_file_path']) #讀取真損益表
    except:
        fs = pd.read_csv(fake_fs_file_path) #讀取假損益表

        # 由於有可能出現公司沒有現金流量表的狀況，所以要做一個 try 的動作
    fake_cfs_file_path = ".\\stock_analyzer\\stock_data\\fake_cfs.csv"
    try: 
        cfs = pd.read_csv(file_path['cfs_file_path']) #讀取真現金流量表
    except:
        cfs = pd.read_csv(fake_cfs_file_path) #讀取假現金流量表


        # 由於有可能出現公司沒有除權息的狀況，所以要做一個 try 的動作
    fake_dr_file_path = ".\\stock_analyzer\\stock_data\\fake_dr.csv"
    try: 
        dr = pd.read_csv(file_path['dr_file_path']) #讀取真除權息結果表
    except:
        dr = pd.read_csv(fake_dr_file_path) #讀取假除權息表
    
    #取得 EPS
    eps = fs[fs['type'] == 'EPS']
    
    # 取得稅後淨利 IncomeAfterTaxes
    # 由於資料裡面有不時會出現IncomeAfterTax，因此需要兩種同時搜尋
    incomeAfterTaxes = fs[fs['type'].isin(['IncomeAfterTaxes', 'IncomeAfterTax'])]
    
    # 取得股東權益 Equity
    equity = bs[bs['type'] == 'Equity']
    #合併股東權益以及稅後淨利表
    
    merge_incomeAfterTaxes_equity = incomeAfterTaxes.merge(equity, on=["date", "stock_id"], how="inner")
    
    """
    條件一 critera_1
    # ROE:  連續5年 > 10% (ROE = 稅後淨利/ 股東權益) => 損益表, 資產負債表
    or 
    # EPS:  連續10年 > 0 (EPS = 稅後淨利/ 發行股數) => 損益表
    """
    
    critera_1 = None
    critera_ROE = 'ROE: 連續' + str(search_criteria['ROE_continue_year']) +'年 > '+ str(math.floor(search_criteria['ROE_criteria']*100)) + '%'
    result_critera_ROE = None
    critera_EPS = 'EPS: 連續' + str(search_criteria['EPS_continue_year']) + '年 > ' + str(math.floor(search_criteria['EPS_criteria']*100))
    result_critera_EPS = None


    """
    篩選
    """
    #篩選 ROE x年的資料
    merge_incomeAfterTaxes_equity.loc[:, 'date'] = pd.to_datetime(merge_incomeAfterTaxes_equity['date'])
    filtered_MIE = merge_incomeAfterTaxes_equity[merge_incomeAfterTaxes_equity['date'].between(x_years_ago(search_criteria['ROE_continue_year']), pd.Timestamp.now())]
    #篩選 EPS x年的資料
    eps.loc[:, 'date'] = pd.to_datetime(eps['date'])
    filtered_eps = eps[eps['date'].between(x_years_ago(search_criteria['EPS_continue_year']), pd.Timestamp.now())]
    
    """
    判斷
    """
    # 判斷 ROE 標準是否有打開
    if search_criteria['ROE'] == True:
        
        condition1_ROE_satisfied = True # 先假設滿足ROE條件
        
        # 檢查資料時間是否滿足 x年的長度
        data_days = (pd.Timestamp.now() - min(filtered_MIE['date']))
        data_years = data_days.days/365 # 計算資料距離現在多少年
        if data_years >= search_criteria['ROE_continue_year'] -1:
            # 判斷 ROE 是否符合連續x年 > y%
            for index, row in filtered_MIE.iterrows():
                if row['value_y'] == 0: # 排除讀取到 fake 資料時的狀況
                    ROE = 0
                else: 
                    ROE = row['value_x']/row['value_y']
                
                if ROE < search_criteria['ROE_criteria']:
                    #沒有符合條件的情況
                    condition1_ROE_satisfied = False
                    result_critera_ROE = '不符合'
                    print('不符合 ' + critera_ROE)
                    break
                else:
                    #符合條件的情況
                    result_critera_ROE = '符合'
        else:
            condition1_ROE_satisfied = False
            result_critera_ROE = '不符合'
            print('不符合 ' + critera_ROE)

    else: 
        condition1_ROE_satisfied = False
        result_critera_ROE = '無啟用'

    # 判斷 EPS 標準是否有打開
    if search_criteria['EPS'] == True:
        
        condition1_EPS_satisfied = True # 先假設滿足EPS條件
        # 檢查資料時間是否滿足 x年的長度
        data_days = (pd.Timestamp.now() - min(filtered_eps['date']))
        data_years = data_days.days/365 # 計算資料距離現在多少年       
        if data_years >= search_criteria['EPS_continue_year'] -1:

            # 判斷 EPS 是否符合連續x年 > y 
            for index, row in filtered_eps.iterrows(): 
                if row['value'] <= search_criteria['EPS_criteria']: 
                    #沒有符合條件的情況
                    condition1_EPS_satisfied = False
                    result_critera_EPS = '不符合'
                    print('不符合 ' +  critera_EPS)
                    break
                else: 
                    #符合條件的情況
                    result_critera_EPS = '符合'
        else:
            condition1_EPS_satisfied = False
            result_critera_EPS = '不符合'
            print('不符合 ' +  critera_EPS)
    else:
        condition1_EPS_satisfied = False
        result_critera_EPS = '無啟用'

    # 進行條件一總合判斷        
    if result_critera_ROE == '無啟用' and result_critera_EPS == '無啟用':
        critera_1 = '無啟用'
        print('**條件一 無啟用') 

    elif condition1_ROE_satisfied or condition1_EPS_satisfied:
        # 符合條件
        critera_1 = 'Pass'
        print("**條件一 成功訊息")
    else:
        # 沒有符合條件
        critera_1 = 'No Pass'
        print("**條件一 不成功訊息")
        pass
        
    
    #彙整條件一的結果
    criteria_c1 = {
        'ROE' : critera_ROE,
        'EPS' : critera_EPS
    }
    result_c1 = {'條件一結果' : critera_1,
                 critera_ROE : result_critera_ROE,
                 critera_EPS : result_critera_EPS}

    """
    條件二
    # 營業活動現金流對比淨利 連 5年 > 80% => 現金流量表, 損益表
    and
    # 資產負債比率 連5年 < 50% => 資產負債表 (負債總額/資產總額 x 100%)
    and
    # 負債權益比率 連5年 < 100% => 資產負債表 (負債總額 /股本總額 x 100%)
    and
    # 配發股利/股息 連10年 > 0 => 除權息結果表
    and
    # 平均股利/股息 > 5% => 除權息結果表
    """
    critera_2 = None
    critera_cashflow = '營業活動現金流對比淨利 連' + str(search_criteria['cashflow_continue_year']) + '年 > ' + str(math.floor(search_criteria['cashflow_criteria']*100)) + '%'
    result_critera_cashflow = None
    critera_liabilities_TA = '資產負債比率 連' + str(search_criteria['liabilities_TA_continue_year']) + '年 < ' + str(math.floor(search_criteria['liabilities_TA_criteria']*100)) + '%'
    result_critera_liabilities_TA = None
    critera_liabilities_CP = '負債權益比率 連' + str(search_criteria['liabilities_CP_continue_year']) + '年 < ' + str(math.floor(search_criteria['liabilities_CP_criteria']*100)) + '%'
    result_critera_liabilities_CP = None
    critera_yeild = '配發股利/股息 連' + str(search_criteria['yeild_continue_year']) + '年 > ' + str(search_criteria['yeild_criteria']*100)
    result_critera_yeild = None
    critera_yeild_AV = '平均股利/股息 > ' + str(math.floor(search_criteria['yeild_AV_criteria']*100)) + '%'
    result_critera_yeild_AV = None

    # 取得營業活動現金流 CashReceivedThroughOperations
    cashReceivedThroughOperations = cfs[cfs['type'] == 'CashReceivedThroughOperations']
    
    #合併營業活動現金流以及稅後淨利表
    merge_CTO_incomeAfterTaxes = cashReceivedThroughOperations.merge(incomeAfterTaxes, on=["date", "stock_id"], how="inner")

    # 取得負債總額 Liabilities
    liabilities = bs[bs['type'] == 'Liabilities']

    # 取得資本總額 TotalAssets
    totalAssets = bs[bs['type'] == 'TotalAssets']

    # 合併負債總額以及資本總額表
    merge_liabilities_totalAssets = liabilities.merge(totalAssets, on=["date", "stock_id"], how="inner")

    # 取得股本總額 CapitalStock
    capitalStock = bs[bs['type'] == 'CapitalStock']

    # 合併負債總額以及股本總額表
    merge_liabilities_capitalStock = liabilities.merge(capitalStock, on=["date", "stock_id"], how="inner")

    # 計算殖利率
    dr["yeild"] = dr["stock_and_cache_dividend"] / dr["before_price"]
    yeild = dr[["date", "stock_id", "yeild"]]

    """
    篩選
    """
    # 篩選出營業活動現金流對比淨利近x年的資料
    merge_CTO_incomeAfterTaxes.loc[:, 'date'] = pd.to_datetime(merge_CTO_incomeAfterTaxes['date'])
    filtered_MCI = merge_CTO_incomeAfterTaxes[merge_CTO_incomeAfterTaxes['date'].between(x_years_ago(search_criteria['cashflow_continue_year']), pd.Timestamp.now())]
    
    # 篩選出資產負債比率近x年資料
    merge_liabilities_totalAssets.loc[:, 'date'] = pd.to_datetime(merge_liabilities_totalAssets['date'])
    filtered_MLT = merge_liabilities_totalAssets[merge_liabilities_totalAssets['date'].between(x_years_ago(search_criteria['liabilities_TA_continue_year']), pd.Timestamp.now())]

    # 篩選負債權益比率近5年資料
    merge_liabilities_capitalStock.loc[:, 'date'] = pd.to_datetime(merge_liabilities_capitalStock['date'])
    filtered_MLC = merge_liabilities_capitalStock[merge_liabilities_capitalStock['date'].between(x_years_ago(search_criteria['liabilities_CP_continue_year']), pd.Timestamp.now())]
    # 篩選配發股利/股息近10年
    yeild.loc[:, 'date'] = pd.to_datetime(yeild['date'])
    filtered_yeild = yeild[yeild['date'].between(x_years_ago(search_criteria['yeild_continue_year']), pd.Timestamp.now())]
    
    """
    判斷
    """
    # 判斷 cashflow 標準是否有打開
    if search_criteria['cashflow'] == True:
        
        condition2_MCI_satisfied = True # 先假設滿足cashflow 條件
        # 檢查資料時間是否滿足 x年的長度
        data_days = (pd.Timestamp.now() - min(filtered_MCI['date']))
        data_years = data_days.days/365 # 計算資料距離現在多少年       
        if data_years >= search_criteria['cashflow_continue_year'] -1:

            # 判斷 營業活動現金流對比淨利 連 x年 > y
            for index, row in filtered_MCI.iterrows():
                if row['value_y'] == 0: #排除讀取到 fake 資料的狀況
                    MCI = 0
                else:
                    MCI = row['value_x']/row['value_y']
                if MCI < search_criteria['cashflow_criteria']:
                    # 不符合的情況
                    condition2_MCI_satisfied = False
                    result_critera_cashflow = '不符合'
                    print('不符合 ' + critera_cashflow)
                    break
                else: 
                    # 符合的情況
                    result_critera_cashflow = '符合'
        else:
            condition2_MCI_satisfied = False
            result_critera_cashflow = '不符合'
            print('不符合 ' + critera_cashflow)            
    else: 
        condition2_MCI_satisfied = True
        result_critera_cashflow = '無啟用'


    # 判斷 liabilities_TA 標準是否有打開
    if search_criteria['liabilities_TA'] == True:

        condition2_MLT_satisfied = True # 先假設滿足liabilities_TA 條件
        # 檢查資料時間是否滿足 x年的長度  
        data_days = (pd.Timestamp.now() - min(filtered_MLT['date']))
        data_years = data_days.days/365 # 計算資料距離現在多少年       
        if data_years >= search_criteria['liabilities_TA_continue_year'] -1:              
        
            #判斷 資產負債比率 連x 年 < y           
            for index, row in filtered_MLT.iterrows():
                if row['value_y'] == 0: #排除讀取到 fake 資料的狀況
                    MLT = 0
                else: 
                    MLT = row['value_x']/row['value_y']
                if MLT > search_criteria['liabilities_TA_criteria']:
                    # 不符合的情況
                    condition2_MLT_satisfied = False
                    result_critera_liabilities_TA = '不符合'
                    print('不符合 ' + critera_liabilities_TA)
                    break
                else:
                    # 符合的情況
                    result_critera_liabilities_TA = '符合' 
        else:
            condition2_MLT_satisfied = False
            result_critera_liabilities_TA = '不符合'
            print('不符合 ' + critera_liabilities_TA)            
    else: 
        condition2_MLT_satisfied = True
        result_critera_liabilities_TA = '無啟用'


    # 判斷 liabilities_CP 標準是否有打開
    if search_criteria['liabilities_CP'] == True:
        
        condition2_MLC_satisfied = True # 先假設滿足 liabilities_CP 條件
        # 檢查資料時間是否滿足 x年的長度 
        data_days = (pd.Timestamp.now() - min(filtered_MLC['date']))
        data_years = data_days.days/365 # 計算資料距離現在多少年       
        if data_years >= search_criteria['liabilities_CP_continue_year'] -1:                  
        
            #判斷 負債權益比率 連x年 < y
            for index, row in filtered_MLC.iterrows():
                if row['value_y'] == 0: #排除讀取到 fake 資料的狀況
                    MLC = 0
                else: 
                    MLC = row['value_x']/row['value_y']
                if MLC > search_criteria['liabilities_CP_criteria']:
                    # 不符合的情況
                    condition2_MLC_satisfied = False
                    result_critera_liabilities_CP = '不符合'
                    print('不符合 ' + critera_liabilities_CP)
                    break
                else: 
                    # 符合的情況
                    result_critera_liabilities_CP = '符合'    
        else:
            condition2_MLC_satisfied = False
            result_critera_liabilities_CP = '不符合'
            print('不符合 ' + critera_liabilities_CP)
    else:
        condition2_MLC_satisfied = True
        result_critera_liabilities_CP = '無啟用'

    
    # 判斷 yeild 標準是否有打開
    if search_criteria['yeild'] == True:

        condition2_yeild_satisfied = True # 先假設符合 yeild 條件
        # 檢查資料時間是否滿足 x年的長度
        data_days = (pd.Timestamp.now() - min(filtered_yeild['date']))
        data_years = data_days.days/365 # 計算資料距離現在多少年       
        if data_years >= search_criteria['yeild_continue_year'] -1:          
            
            #判斷 配發股利/股息 連x年 > y
            for row in filtered_yeild['yeild']:
                if row <= search_criteria['yeild_criteria']:
                    # 不符合的情況
                    condition2_yeild_satisfied = False
                    result_critera_yeild = '不符合'
                    print('不符合 ' + critera_yeild)
                    break
                else:
                    # 符合的情況
                    result_critera_yeild = '符合'
        else:
            condition2_yeild_satisfied = False
            result_critera_yeild = '不符合'
            print('不符合 ' + critera_yeild)
    else: 
        condition2_yeild_satisfied = True
        result_critera_yeild = '無啟用'

    
    # 判斷 yeild_AV 標準是否有打開
    if search_criteria['yeild_AV'] == True:

        
        condition2_AverageYeild_satisfied = True
        # 檢查資料時間是否滿足 x年的長度
        data_days = (pd.Timestamp.now() - min(filtered_yeild['date']))
        data_years = data_days.days/365 # 計算資料距離現在多少年   
        if data_years >= search_criteria['yeild_continue_year'] -1:
            
            # 判斷是季配息還是年配息
            if len(filtered_yeild['date']) <= search_criteria['yeild_continue_year']:
                mean_yeild = filtered_yeild['yeild'].mean() #年配息
            elif search_criteria['yeild_continue_year'] < len(filtered_yeild['date']) <= search_criteria['yeild_continue_year']*2:
                mean_yeild = filtered_yeild['yeild'].mean()*2 #半年配
            else:
                 mean_yeild = filtered_yeild['yeild'].mean()*4 #季配息

            #判斷 平均股利/股息 > y
            if mean_yeild < search_criteria['yeild_AV_criteria']:
                # 不符合的情況
                condition2_AverageYeild_satisfied = False
                result_critera_yeild_AV = '不符合'
                print('不符合 ' + critera_yeild_AV)
            else:
                # 符合的情況
                result_critera_yeild_AV = '符合'
        else:
            condition2_AverageYeild_satisfied = False
            result_critera_yeild_AV = '不符合'
            print('不符合 ' + critera_yeild_AV)
    else:
        condition2_AverageYeild_satisfied = True
        result_critera_yeild_AV = '無啟用'


    # 進行條件二總合判斷 
    if result_critera_cashflow == '無啟用' and result_critera_liabilities_TA == '無啟用' and result_critera_liabilities_CP == '無啟用' and result_critera_yeild == '無啟用' and result_critera_yeild_AV == '無啟用':
        critera_2 = '無啟用'
        print("**條件二 無啟用")

    elif condition2_MCI_satisfied and condition2_MLT_satisfied and condition2_MLC_satisfied and condition2_yeild_satisfied and condition2_AverageYeild_satisfied:
        # 符合條件
        critera_2 = 'Pass'
        print("**條件二 成功訊息")
    else:
    # 沒有符合條件
        critera_2 = 'No Pass'
        print("**條件二 不成功訊息")
        pass

    #彙整條件二的結果，然後傳出
    criteira_c2 = {
        'cashflow' : critera_cashflow,
        'liabilities_TA' : critera_liabilities_TA,
        'liabilities_CP' : critera_liabilities_CP,
        'yeild' :  critera_yeild,
        'yeild_AV' : critera_yeild_AV
    }
    result_c2 = { '條件二結果' : critera_2,
                critera_cashflow : result_critera_cashflow,
                critera_liabilities_TA : result_critera_liabilities_TA,
                critera_liabilities_CP : result_critera_liabilities_CP,
                critera_yeild : result_critera_yeild,
                critera_yeild_AV : result_critera_yeild_AV
                }

    return result_c1, result_c2, criteria_c1, criteira_c2


# 時間點製造功能
def x_years_ago(years):
    x_years_ago = pd.Timestamp.now() - pd.DateOffset(years=years) 
    return x_years_ago