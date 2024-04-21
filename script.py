import pandas as pd
# 找出所有股票代號
stocklist_file_path = ".\\stock_analyzer\\stock_data\\StockList.csv"
stock_list = pd.read_csv(stocklist_file_path)
stock_id = []
  # 由於有兩種股票代號格式在 StockList ，而我們只取有等號的資訊
for item in stock_list['代號']: 
    if "=" in item: # 含有等號的資料
        item = item.replace("=","")[1:-1]
        stock_id.append(item)

stock_id = stock_id[192:] # 從公司股票開始搜尋 (排除ETF)

# 需要搜尋的條件以及範圍
search_criteria = {
'range' : stock_id,
# 條件一
'ROE' : True,
'ROE_continue_year' : 5,
'ROE_criteria' : 0.1, 
'EPS' : True,
'EPS_continue_year' : 5,
'EPS_criteria' : 0,
# 條件二
'cashflow' : True,
'cashflow_continue_year' : 5,
'cashflow_criteria' : 0.8,
'liabilities_TA' : False,
'liabilities_TA_continue_year' : 5,
'liabilities_TA_criteria' : 0.5,
'liabilities_CP' : False,
'liabilities_CP_continue_year' : 5,
'liabilities_CP_criteria' : 1,
'yeild' : True,
'yeild_continue_year' : 5,
'yeild_criteria' : 0,
'yeild_AV' : True,
'yeild_AV_criteria' : 0.03,
}
'''
來自資料上的限制:
1. 目前資料最早下載的時間為2019/3/31，因此需要調整連續年小於4，否則會跳不符合
'''


# 預先建立一個空的結果空間，給後續填入資料使用
result = {}

import os
from functools import partial
from catcher import catcher

print(search_criteria['range'])
# 依次掃描search_criteria 中 range 裡面的股票代號
for stock_id in search_criteria['range']:

  # 判斷檔案是否已經建立
  name = stock_id
  print('name in list: ', name)

  # 從結果空間當中建立一個空的以 stock_id 為名的空間
  result[stock_id] = {} 

  bs_file_path = ".\\stock_analyzer\\stock_data\\{name}_bs.csv".format(name=name)
  cfs_file_path = ".\\stock_analyzer\\stock_data\\{name}_cfs.csv".format(name=name)
  fs_file_path = ".\\stock_analyzer\\stock_data\\{name}_fs.csv".format(name=name)
  dr_file_path = ".\\stock_analyzer\\stock_data\\{name}_dr.csv".format(name=name)
  file_path = {'bs_file_path': bs_file_path, 
             'cfs_file_path' : cfs_file_path, 
             'fs_file_path' : fs_file_path,
             'dr_file_path' : dr_file_path
             }


  #判斷若檔案尚未建立，則執行Catcher，否則不重新執行 (以是否有資產負債表判斷)
  if not os.path.exists(bs_file_path):
      print('bs_file_path does not exists')

      # 觸發 Catcher 開始搜尋
      fatch_data = partial(catcher, stock_id = stock_id)
      bs, cfs, fs, dr, sd, si = fatch_data()

        #寫入已建立的檔案
      bs.to_csv(bs_file_path,index=False)
      cfs.to_csv(cfs_file_path,index=False)
      fs.to_csv(fs_file_path,index=False)
      dr.to_csv(dr_file_path, index=False)

      print('資料建立完成')

  """"
  搜尋資料: 
    資產負債表(bs)、現金流量表(cfs)、綜合損益表(fs)、成交日資訊(sd)、台股更新資料(si)、下載除權息表(dr)
  """


  # 啟動 Analyzer 並匯入資料
  from analyzer import analyzer

  analyze_data = partial(analyzer)
  result_c1, result_c2, criteria_c1, criteira_c2 = analyze_data(file_path, search_criteria)

  # 將結果放入 result[stock_id] 當中
  result[stock_id]['criteria_1'] = result_c1
  result[stock_id]['criteria_2'] = result_c2


# 使用Json格式將儲存分析完的資訊
import json

filename = '.\\stock_analyzer\\analyzed_result\\result.txt'
with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


# 驅動 Renderer 
from renderer import renderer 
render_data = partial(renderer)
render_data(criteria_c1, criteira_c2)



#測試區