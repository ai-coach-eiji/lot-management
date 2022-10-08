import pandas as pd

def check_error(prd_df):
    # エラーのidxを検出（在庫がマイナスになっている行番号を特定する）
    minus_list = prd_df[pd.to_numeric(prd_df['在庫']) < 0].index.values.tolist() # pd.to_numeric()でint64に変換
    print("[check_error func] 在庫がマイナスのidxリスト: ", minus_list) #DEBUG用
    return minus_list, len(minus_list)