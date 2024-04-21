# 負責依照來自於 sript.py 的 search_criteria，然後透過API 取得相關的資料
from FinMind.data import DataLoader

# 主要驅動API程式
def catcher(stock_id):
    print('catcher is working')
    api = DataLoader()

    # 下載資產負債表
    bs = api.taiwan_stock_balance_sheet(
        stock_id= stock_id,
        start_date='2019-03-31',
    )

    # 下載現金流量表
    cfs = api.taiwan_stock_cash_flows_statement(
        stock_id= stock_id,
        start_date='2019-03-31',
    )
    
    # 下載綜合損益表
    fs = api.taiwan_stock_financial_statement(
        stock_id= stock_id,
        start_date='2019-03-31',
    )

    # 下載除權息表
    dr = api.taiwan_stock_dividend_result(
        stock_id= stock_id,
        start_date='2019-03-31',
    )  
    
    # 下載成交資訊
    sd = api.taiwan_stock_daily(
        stock_id= stock_id,
        start_date='2020-04-02',
        end_date='2020-04-12'
    )

    # 下載台股前一天更新資料
    si = api.taiwan_stock_info()
    
    return bs, cfs, fs, dr, sd, si
    """
    for item in df:
        if item["type"] == "IncomeAfterTaxes":
            pretax_profit_value = df.iloc[1]["value"]
            break  # Exit the loop after finding the first matching item

    if pretax_profit_value:
        print(f"Value for '稅前淨利（淨損）': {pretax_profit_value}")
    else:
        print("Value for '稅前淨利（淨損）' not found.")


    """