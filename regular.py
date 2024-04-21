from FinMind.data import DataLoader
import FinMind
import pandas as pd

# stockmap 的路徑
stockmap_file_path = ".\\stock_analyzer\\stock_data\\stockmap.csv"

# 檢查是否有 stockmap 檔案的存在，如果沒有，下載一份
import os
if not os.path.exists(stockmap_file_path):
      print('stockmap_file_path does not exists')
      api = DataLoader()
      download_data = api.taiwan_stock_info()
      download_data.to_csv(stockmap_file_path,index=False)
else:
      print('stockmap_file_path existed')
      

# 測試區

stock_id = pd.read_csv(stockmap_file_path)

stock_id = stock_id.loc[stock_id['type'].isin(['twse'])]


