#!/user/bin/env python
# coding: utf-8

import pandas as pd

from ..constant.item import item_dict

def extract_as_df(gs_values):
    # gsheetの値をpdDataFrameに変換
    df = pd.DataFrame(gs_values)
    #columns = [str(i) for i in range(0, len(df.columns))]
    columns = df[:1].values.tolist()[0]
    df.columns = columns

    df.drop(0, inplace=True) # 0行目（アルファベット文字のヘッダー）をドロップ
    df.replace([''], [None], inplace=True)
    return df

def extract_prd_date(d_contents):
    # QR_Noを日付文字列に変換
    lot_year = d_contents[:4]
    lot_month = d_contents[4:6]
    lot_day = d_contents[6:8]

    prd_date = f'{lot_year}/{lot_month}/{lot_day}' # 製造日(スラッシュ表記)
    print("QR_Noから製造日を取得: ", prd_date)
    return prd_date

def item_id_name(d_contents):
    # QR_Noから製造種目ID（QR_No下2桁）と製造種目名を取得
    item_n = get_item_id(d_contents)
    item_name = get_item_name(item_n)
    
    print("製造種目ID, 製造種目名: ", item_n, item_name)
    return item_n, item_name

def get_item_id(d_contents):
    # QR_Noから製造種目ID（QR_No下2桁）を取得
    return d_contents[-2:]

def get_item_name(item_n):
    # 製造種目IDから製造種目名を取得
    return item_dict[item_n] # item_dict（製造種目の辞書）: constantパッケージで定義

def get_idx(df, column_name, target):
    # target（検索したい値）が列（column_name）にある場合、その最初の行番号（idx）を取得
    target_idx = df.index[df[column_name] == target].tolist() # targetと一致するのは何行目か（ = 行のidxを取得）
    target_idx = int(target_idx[0]) # 最初のidxのみを取得
    print("指定値に一致した行番号: ", target_idx) # DEBUG用（ToDo index out of range が出たら、editで追加したQR_Noと一致していない可能性あり）
    return target_idx

def get_idx_list(df, column_name, target):
    # target（検索したい値）が列（column_name）にある場合、そのすべての行番号（idx）をリストで取得
    target_idx_list = df.index[df[column_name] == target].tolist() # targetと一致するのは何行目か（ = 行のidxを取得）
    return target_idx_list

def get_last_idx(df, column_name):
    # 最終行の取得
    last_idx = None
    none_list = df[df[column_name].isnull()].index.tolist()

    if none_list == []: # Noneデータがない場合は最終行に続いてappendする
        df.loc[len(df)+1] = [None for _ in range(len(df.columns))]
        #print("新しい行を追加後のdf: \n", df) # DEBUG用
        last_idx = df[-1:].index.tolist()[0]
    else:
        last_idx = none_list[0] # そうでない場合はNoneデータのはじめに値を追加していく
    print(f"シートの最終行: {last_idx} を取得しました")
    return last_idx

def column_as_list(df, column_name):
    # dfシートの列名: column_name をリストとして抽出する
    return df[column_name].values.tolist()

def edit_shipping_byhand(ship_df, edit_date, post_dict, column_name="タイムスタンプ"):
    # /lot/edit/ にて、出荷シートの情報を手動入力できる
    last_idx = get_last_idx(ship_df, column_name) # タイムスタンプ列の最終行の番号を取得（ここに編集内容を記載）

    ship_df.at[last_idx, column_name] = edit_date # 編集を行った時のタイムスタンプ
    ship_df.at[last_idx, "QR_No"] = post_dict["QR_No"]
    ship_df.at[last_idx, "出荷日"] = post_dict["ship_date"]
    ship_df.at[last_idx, "出荷先"] = post_dict["出荷先"]
    ship_df.at[last_idx, "出荷個数"] = post_dict["ice_count"]
    ship_df.at[last_idx, "反映済み"] = 0 # 未反映なので0
    #print("更新後の出荷シート: ", ship_df) #DEBUG用

    return last_idx

def create_prd(prd_df, writing_date, post_dict, column_name="タイムスタンプ"):
    # /lot/product/ にて、製造シートに製造情報を記入
    last_idx = get_last_idx(prd_df, column_name)

    prd_df.at[last_idx, column_name] = writing_date # タイムスタンプ
    prd_df.at[last_idx, "QR_No"] = post_dict["QR_No"]
    prd_df.at[last_idx, "製造日"] = post_dict["prd_date"]
    prd_df.at[last_idx, "製造種目"] = post_dict["prd_kind"]
    prd_df.at[last_idx, "製造個数"] = post_dict["ice_count"] # 製造個数
    prd_df.at[last_idx, "在庫"] = post_dict["ice_count"] # 製造個数と同じ数を登録
    print(prd_df) # DEBUG用

    updated_row = prd_df.loc[last_idx].values.tolist()[:6] # 更新した値を取得（Googleシート用）
    return last_idx, updated_row