#!/user/bin/env python
# coding: utf-8

import pandas as pd
import time

from ..constant.shipping import write_ship_columns_list, write_gshipsheet_columns_list
from .extract import get_idx, get_last_idx

from ..authentication.gsheet import get_worksheet_and_id, get_g_values

def extract_one_column(gs_values, column_name):
    df = pd.DataFrame(gs_values)
    #columns = [str(i) for i in range(0, len(df.columns))]
    columns = df[:1].values.tolist()[0]
    df.columns = columns

    df.drop(0, inplace=True) # 0行目をドロップ
    df.replace([''], [None], inplace=True)

    registered_numbers = df[column_name]
    return registered_numbers

def write_only_shipdest(ship_df, ship_dest, scan_date):
    # df出荷シートの出荷先列を更新

    ship_dest_series = ship_df["出荷先"] # 出荷先列の値を取得
    # gs_values = get_g_values("出荷シート") # TEST 22/10/6
    # ship_dest_series = extract_one_column(gs_values, "出荷先") # TEST 22/10/6
    
    none_idx_list = ship_df[ship_dest_series.isnull()].index.tolist() # 出荷先列の空セルのidxを取得
    print('出荷先列の空セルのidxリスト: ', none_idx_list)
    
    ship_date_series = ship_df["出荷日"] # 出荷日列の値を取得
    ship_candidate_idx_list = ship_df.index[(ship_date_series == str(scan_date))].tolist() # スキャンした日付が出荷日列にあればそのidxを取得

    shipdest_last_idx = get_last_idx(ship_df, "出荷先") # 出荷シートの出荷列の最終行番号を取得

    updated_list = None
    empty_list = [] # 出荷先が記入されていない行番号がある場合に使用

    if none_idx_list == []: # 18行（種類_データ列のせいで、行数が無駄にNoneとしてカウントされるため）より多い時の処理
        print('候補なし（商品の出荷日はすべて記入済み）')
    else:
        updated_list = []
        for idx in none_idx_list: # 空セルのidxを順に見ていく

            print('') # DEBUG用
            if idx in ship_candidate_idx_list: # 日付がスキャン日時と一致していれば処理
                print(f'{idx}行目に{ship_dest}を追加します（{scan_date}）') # DEBUG用
                ship_df.at[idx, "出荷先"] = ship_dest

                updated_list.append(idx)
            else:
                print(f'空欄ですが、日付が一致しません（{idx}行目）') # DEBUG用
                empty_list.append(idx)

                # if idx == shipdest_last_idx: # 候補idxと空セルのidxが一致した場合はそこで処理を終了
                #     print(f'出荷先を入力できる候補のidx(={shipdest_last_idx})を超えましたので、処理を終了します') # DEBUG用
                #     break
        
        print('出荷先を追加した結果: \n', ship_df)
    return updated_list, empty_list

def write_shipdest_gsheet(ship_sheet, ship_dest, update_list):
    # Google出荷シートの出荷先列を更新
    for idx in update_list:
        ######################### シート更新 #########################
        ship_sheet.update_acell(f'D{idx+1}', str(ship_dest)) # 出荷シートの出荷先（D列）を更新
        ######################### 更新ここまで #########################

def write_shipping(ship_df, scan_temp):
    # 出荷シートにスキャンした商品の情報を記録し、記録したidxを出力
    time_column = "タイムスタンプ"

    ship_add_idx = get_last_idx(ship_df, time_column) # 出荷シートに記載したい（最終の）行番号を取得
    #print("シートの次の位置に値を追加（Noneであることが正しい）: ", ship_df.at[ship_add_idx, time_column]) # DEBUG用

    ship_df = write_row_shipping(scan_temp, ship_df, ship_add_idx) # 出荷シートにscan_tempを記載
    #print(f'変更後: \n{ship_df}') # DEBUG用
    return ship_add_idx

def write_row_shipping(scanned_list, ship_df, idx):
    # スキャンした1つの商品情報（出荷先は含まない）をdf出荷シートに記載する
    for c, data in zip(write_ship_columns_list, scanned_list): # リストの順番で値を記録
        ship_df.at[idx, c] = data
    return ship_df

def write_shipping_gsheet(scan_temp, ship_sheet, idx):
    # Google出荷シートにスキャンした商品情報を記載する
    for c, data in zip(write_gshipsheet_columns_list, scan_temp): # リストの順番で値を追加していく
        ######################### シート更新 #########################
        ship_sheet.update_acell(f'{c}{idx+1}', str(data)) # 出荷シートの A, B, C, E, F列を更新
        ######################### 更新ここまで #########################

def write_scanned_item(flag, ship_df, ship_sheet, scanned_list):
    # /lot/ で、 値が一致している場合はスキャンした情報をgsheetに書き込む

    if flag: # 一致した場合は出荷シートを更新
        ship_add_idx = write_shipping(ship_df, scanned_list) # dfに出荷情報を記録

        ######################### シート更新 #########################
        write_shipping_gsheet(scanned_list, ship_sheet, ship_add_idx) # gsheetに出荷情報を記載
        ######################### 更新ここまで #########################
    else:
        print('値が一致しなかったため、gsheetへの書き込みは行われません') # DEBUG用

def write_shipping_byhand(ship_sheet, edit_date, post_dict, last_idx):
    # /lot/edit/ で、入力した情報をGoogle出荷シートに記録
    
    ############################### シート更新 ############################### # 手書きでシートを更新
    ship_sheet.update_acell(f'A{last_idx+1}', str(edit_date))
    ship_sheet.update_acell(f'B{last_idx+1}', str(post_dict["QR_No"]))
    ship_sheet.update_acell(f'C{last_idx+1}', str(post_dict["ship_date"]))
    ship_sheet.update_acell(f'D{last_idx+1}', str(post_dict["出荷先"]))
    ship_sheet.update_acell(f'E{last_idx+1}', str(post_dict["ice_count"]))
    ship_sheet.update_acell(f'F{last_idx+1}', str(0))
    ############################### 更新ここまで ###############################

    sheet_dest_updated = ship_sheet.acell(f'D{last_idx+1}').value
    #print("更新後の出荷シート上の出荷先: ", sheet_dest_updated) # DEBUG用

def subtract_stock_gsheet(prd_sheet, subtract_dict):
    # /lot/stock/ で、Google製造シートの在庫（F）列を更新
    for idx, v in subtract_dict.items():
        prd_sheet.update_acell(f'F{idx+1}', str(v))

def update_loginfo_gsheet(ship_sheet, not_logged_idx):
    # /lot/stock/ で、Google出荷シートの反映済み列の数字を1に変更
    for idx in not_logged_idx:
        ship_sheet.update_acell(f'F{idx+1}', str(1))

def write_stock_gsheet(prd_sheet, updated_stock_ids, latest_stock_dict):
    # /lot/stock/ で、Google製造シートの冷凍庫内個数を更新
    ################################# シート更新 #################################
    for idx, (k, v) in zip(updated_stock_ids, latest_stock_dict.items()):
        prd_sheet.update_acell(f'I{idx+1}', str(v)) # 製造シートの冷凍庫内個数（I列）を更新
    ################################# 更新ここまで #################################

def write_allstock_gsheet(prd_sheet, stock_count):
    # /lot/stock/ で、Google製造シートの合計値を更新
    sum_idx = 1
    ######################## シート更新 ######################
    prd_sheet.update_acell(f'J{sum_idx+1}', str(stock_count)) # Google製造シートの合計値（J2）を更新
    ######################## 更新ここまで #####################

def write_error_gsheet(prd_sheet, error_n):
    # /lot/stock/ で、Google製造シートのエラー数を更新
    ######################## シート更新 ######################
    prd_sheet.update_acell(f'K2', str(error_n)) # Google製造シートのエラーの数（K2）を更新
    ######################## 更新ここまで #####################

def write_prd_gsheet(prd_sheet, scan_date, idx, updated_row):
    # /lot/product/ で、Google製造シートに製造情報を記入
    g_list = ['A', 'B', 'C', 'D', 'E', 'F'] # googleシートの更新する列を順にリストに格納

    for n, value in zip(g_list, updated_row):
        ######################### シート更新 #########################
        prd_sheet.update_acell(f'{n}{idx+1}', str(value)) # 製造シートに情報を記入
        ######################### 更新ここまで #########################

def write_prddone_gsheet(prd_gsheet_dict, sheet):
    # /lot/download/ で、製造シートから切り取った情報をGoogleの製造出荷完了シートに記載する
    columns_list = ["A", "B", "C", "D", "E", "F"] # [QR_No, 出荷日, 出荷先, row_idx]

    for idx, from_prd_list in prd_gsheet_dict.items():
        for c, data in zip(columns_list, from_prd_list): # 上記リストの順番で値を追加していく
            ######################### シート更新 #########################
            sheet.update_acell(f'{c}{idx+1}', str(data))     # Google製造出荷完了シートに切り取った製造情報を記載
            ######################### 更新ここまで #########################
        time.sleep(30)

def write_shipdone_gsheet(ship2done_forGoogle_list, sheet):
    # /lot/download/ で、出荷シートから切り取った情報をGoogleの製造出荷完了シートに記載する
    columns_list = ["H", "I", "J", "K"] # [QR_No, 出荷日, 出荷先, row_idx]

    for ship_dict in ship2done_forGoogle_list:
        for idx, from_ship_list in ship_dict.items():
            for c, data in zip(columns_list, from_ship_list): # 上記リストの順番で値を追加していく
                print(f'{c}{idx}', str(data)) # DEBUG用
                ######################### シート更新 #########################
                sheet.update_acell(f'{c}{idx+1}', str(data))     # Google製造出荷完了シートに切り取った出荷情報を記載
                ######################### 更新ここまで #########################
            time.sleep(30)

def shift_prd_gsheet(prd_df, prd_zero_list):
    # /lot/download/ で、Google製造シートの在庫が0の行をすべて上につめる
    if prd_zero_list != []:
        for e in range(len(prd_zero_list)): # 製造シートの在庫が0だった行の個数分だけループ
            prd_sheet, prd_df, prd_sheetId = get_worksheet_and_id("製造シート")
            g_idx = get_idx(prd_df, "在庫", '0') # つめる度にidxがズレるため、毎回在庫が0の在庫のidxを特定する
            shift_row_gseet(prd_sheet, prd_sheetId, g_idx)

            print(f'{prd_zero_list[e]}の削除が終わりました. 10秒休止..') # DEBUG用
            time.sleep(10)

def shift_ship_gsheet(ship_df, qr_idx_dict):
    # /lot/download/ で、Google出荷シートの在庫が0の行をすべて上につめる
    for qr, ship_zero_list in qr_idx_dict.items(): # k: QR_No, v: ship_zero_list（出荷シートの在庫が0のすべてのidx）
        if ship_zero_list != []:
            for i in range(len(ship_zero_list)): # 出荷シートの在庫が0だった各QR_Noの個数（行数）分だけループ
                ship_sheet, ship_df, ship_sheetId = get_worksheet_and_id("出荷シート")
                g_idx = get_idx(ship_df, "QR_No", qr) # つめる度にidxがズレるため、毎回在庫が0のQR_Noのidxを特定する
                shift_row_gseet(ship_sheet, ship_sheetId, g_idx) # 対象のの行番号(=g_idx)を1行つめる
                if i > 0 and i % 5 == 0:
                    print(f'{i}行目まで削除しました. 10秒休止..') # DEBUG用
                    time.sleep(10)
        print(f'{qr}の削除が終わりました') # DEBUG用

def shift_row_gseet(spreadsheet, sheetId, idx):
    # /lot/download/ で、Google出荷シートの1行を上につめる（行番号: idxを指定する）
    requests = [
        {
            'deleteRange': {
                'range': {
                    'sheetId': sheetId,
                    'startRowIndex': idx, # 0スタートなのでdfと同じidxで良い
                    'endRowIndex': idx+1,
                    'startColumnIndex': 0, # 出荷シート&製造シートなので0:6列（A~F）は固定
                    'endColumnIndex': 6,
                },
                'shiftDimension': 'ROWS',
            }
        }]
    spreadsheet.batch_update({'requests': requests})