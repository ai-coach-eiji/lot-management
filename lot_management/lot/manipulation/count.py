import pandas as pd
import numpy as np

from .extract import get_idx

def get_nlogged_dict(ship_df, not_logged_idx):
    # 出荷シートにあるQR_Noごとの出荷個数を調べる（stock viewで使用）
    not_logged_dict = {}
    for i in not_logged_idx:
        not_logged_qr = ship_df.at[i, "QR_No"]
        count = ship_df.at[i, "出荷個数"]

        if not_logged_qr not in not_logged_dict: # QR_Noが無い場合は辞書に登録
            not_logged_dict[not_logged_qr] = int(count)
        else: # すでにある場合は辞書の値に加算していく
            already_c = not_logged_dict[not_logged_qr]
            count = already_c + int(count)
            not_logged_dict[not_logged_qr] = count
    return not_logged_dict

def subtract_stock(prd_df, diff_dict):
    # 出荷シートの出荷個数に応じた個数を製造シートから減算（stock viewで使用）
    subtract_dict = {} # googleシート更新用の辞書を用意
    for k, v in diff_dict.items():
        idx = get_idx(prd_df, "QR_No", k) # 各QR_Noのidxを取得
        stock_now = prd_df.at[idx, "在庫"]
        new_stock = int(stock_now) - v # 製造シートの在庫 マイナス 出荷シートの出荷個数
        prd_df.at[idx, "在庫"] = new_stock
        subtract_dict[idx] = new_stock
    return prd_df, subtract_dict

def update_loginfo(ship_df, not_logged_idx): # stock viewで使用
    # 出荷シートの該当する在庫を更新したら、 
    # 反映済み列の数字を1（反映したこと示す）に変更
    for i in not_logged_idx:
        ship_df.at[i, "反映済み"] = str(1)
    return ship_df

def calc_latest_stock(prd_df): # stock viewで使用
    # 製造シートの在庫を計算

    # 数字を含めた値が文字列になっているため、整数に変換
    prd_df['在庫'] = pd.to_numeric(prd_df['在庫'], errors='coerce').astype('Int64') # Noneは<NA>に置き換えられるが使わない値なのでそのままにしている
    #print(prd_df['在庫']) # DEBUG用
    group_df = prd_df.groupby('製造種目').agg({'在庫': np.sum})
    #print("製造種目ごとの個数: ", group_df) # DEBUG用

    latest_stock_dict = group_df.to_dict()['在庫'] # 各アイスの在庫を取得
    stock_count = group_df.sum().values.tolist()[0] # 在庫の合計を取得
    print(f'最新の在庫状況: \n{latest_stock_dict}, \n合計: {stock_count}') # DEBUG用
    return latest_stock_dict, stock_count

def write_item_stock(prd_df, latest_stock_dict): # stock viewで使用
    # 冷凍庫内個数を更新

    #print("更新前の冷凍庫内個数: \n", prd_df["冷凍庫内個数"]) # DEBUG用
    updated_stock_ids = [] # Gooleシート更新用
    for k, v in latest_stock_dict.items():
        print("[write_item_stock func] k: ", k) # DEBUG用
        idx = get_idx(prd_df, "冷凍庫内種類", k) # 更新する冷凍庫内種類のidxを調べる
        updated_stock_ids.append(idx)

        prd_df.at[idx, "冷凍庫内個数"] = v # 最新の在庫状況（辞書）で製造シートを更新
    #print("更新後の冷凍庫内個数: \n", prd_df["冷凍庫内個数"]) # DEBUG用
    return prd_df, updated_stock_ids

def write_prd_allstock(prd_df, stock_count): # stock viewで使用
    # 製造シートの冷凍庫内個数に反映
    sum_idx = 1
    prd_sum_now = prd_df.at[sum_idx, "合計"]
    #print(f"更新前のアイス合計: {prd_sum_now}") # DEBUG用

    prd_df.at[sum_idx, "合計"] = stock_count
    prd_sum_after = prd_df.at[sum_idx, "合計"]
    #print(f"更新後のアイス合計: {prd_sum_after}") # DEBUG用
    return prd_df

def write_error(prd_df, error_n):
    #print("エラーの数更新前: \n", prd_df.at[1, "エラー"]) # DEBUG用
    prd_df.at[1, "エラー"] = error_n

    #print("エラーの数更新後: \n", prd_df.at[1, "エラー"]) # DEBUG用