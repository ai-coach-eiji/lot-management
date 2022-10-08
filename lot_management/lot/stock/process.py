# stock view の処理を担当

from ..constant.item import item_dict

from ..authentication import gsheet as gs
from ..manipulation.extract import column_as_list, get_idx_list
from ..manipulation.check import check_error
from ..utils2.chart import create_bar_chart
from ..utils2.draw import draw_msg, reference_item, draw_red

from ..manipulation.count import get_nlogged_dict, subtract_stock, update_loginfo, write_error, calc_latest_stock, write_item_stock, write_prd_allstock
from ..manipulation.write import subtract_stock_gsheet, update_loginfo_gsheet, write_error_gsheet, write_stock_gsheet, write_allstock_gsheet

################################## GET ##################################

def create_stock_dict(stock_list):
    # 在庫の辞書を作成（アクセスがある度に数を取得する必要があるため）
    stock_items = {}
    for (k, v), n in zip(item_dict.items(), stock_list): # item_dict（ID: 製造種目名）
        stock_items[v] = n
    return stock_items # k: 製造種目, v: 在庫数

def get_stock(params):
    # 在庫を取得し、辞書に格納（stock view のメイン処理）
    prd_df, prd_sheet = gs.get_sheet_values("製造シート") # シート名からその値を取得（pd用とgsheet更新用）
    stock_list = column_as_list(prd_df, "冷凍庫内個数") # 冷凍庫内個数列をリストとして抽出

    stock_items = create_stock_dict(stock_list) # 在庫辞書の作成（key: 製造種目, value: 在庫数）
    params['item_stock'] = stock_items

    # plot_div = create_bar_chart(stock_items) # 棒グラフを作成（オプション）
    # params['plot_div'] = plot_div

    sum_value = column_as_list(prd_df, "合計") # 合計列をリストとして抽出
    params['item_sum'] = sum_value[0] # 先頭の値を使用（idx: 0）

    error_list, error_n = check_error(prd_df) # エラーのidxリストを返す
    params['item_error'] = error_n
    
    red_list = draw_red(prd_df, error_list) # 在庫が0の製造種目を特定する（赤で表示するために）
    params['red_list'] = red_list
    return params, error_n

################################## GET ##################################


################################## POST ##################################

def check_registered(params, ship_df, ship_sheet, prd_df, prd_sheet): # ToDo: 出荷先が記入されていない行番号は除外
    # 出荷シートの反映済み列に0（製造シートにまだ反映していない商品）がある場合
    if '0' in ship_df.groupby("反映済み").groups.keys():
        not_logged_idx_list = ship_df.groupby("反映済み").get_group('0').index # 出荷シートにある、まだ反映されていない商品のidxを取得
        #print("まだ反映されていない商品のidx リスト: \n", not_logged_idx_list) # DEBUG用

        not_logged_dict = get_nlogged_dict(ship_df, not_logged_idx_list) # 反映されていないQR_Noごとの出荷個数を取得
        print("QR_Noごとの出荷個数（すべて反映済みの場合はNone）: \n", not_logged_dict)

        if not_logged_dict is not None: # 出荷シート内の商品がすべて（製造シートに）反映済みの場合は not_logged_dict は None になる
            update_prd_stock(prd_df, prd_sheet, not_logged_dict) # 製造シートの在庫列を更新
            update_registered_column(ship_df, ship_sheet, not_logged_idx_list) # 出荷シートの反映済み列を更新
            params["stock_message"] = "製造種目の庫内在庫を更新しました" # 画面に表示する文章
    else:
        error_idx_list, error_n = check_error(prd_df) # 製造シートの在庫列にマイナス(エラー)がないか確認
        if error_idx_list != []:
            for i in error_idx_list: # 在庫のエラーの数だけ確認
                prd_n = prd_df.at[i, '製造個数']
                shipped_sum = calc_item_shipped(ship_df)
                current_stock_n = int(prd_n) - shipped_sum # 現在の在庫数 = 製造個数 - 出荷個数
                update_prd_n(prd_df, prd_sheet, i, current_stock_n) # 在庫数を更新

            params["stock_message"] = "製造シートの在庫数を修正しました"
            print('製造シートにエラーがあります') # DEBUG用
        else:
            params["stock_message"] = "すべての製造種目は既に反映済みです"
            print('出荷シート内のすべての商品は、製造シートの在庫個数に反映済みです') # DEBUG用

    return params, prd_df, prd_sheet

def update_prd_n(prd_df, prd_sheet, idx, current_stock_n):
    # 在庫数にエラーがあった場合、その更新で使用する（出荷シートの余分な行数を削除すればOK）
    prd_df.at[idx, '在庫'] = current_stock_n
    ######################### シート更新 #########################
    prd_sheet.update_acell(f'F{idx+1}', str(current_stock_n))
    ###################### シート更新ここまで ######################

def calc_item_shipped(ship_df):
    # 出荷済みの個数をカウント（製造種目にエラーがあった場合に使用する）
    shipped_idx_list = get_idx_list(ship_df, "反映済み", '1')
    shipped_sum = 0
    for i in shipped_idx_list:
        n = ship_df.at[i, '出荷個数']
        shipped_sum += int(n)
    return shipped_sum

def update_prd_stock(prd_df, prd_sheet, not_logged_dict):
    # 製造シートの在庫列を更新
    prd_df, subtract_dict = subtract_stock(prd_df, not_logged_dict) # 製造シートの在庫（F）列を更新
    ######################### シート更新 #########################
    subtract_stock_gsheet(prd_sheet, subtract_dict) # Google製造シートの在庫（F）列を更新
    ######################### 更新ここまで #########################

    #print("更新後製造シート: \n", prd_df) # DEBUG用

def update_registered_column(ship_df, ship_sheet, not_logged_idx_list):
    # 出荷シートの反映済み列を更新
    ship_df = update_loginfo(ship_df, not_logged_idx_list) # 出荷シートの反映済み（F）列を更新
    ######################### シート更新 #########################
    update_loginfo_gsheet(ship_sheet, not_logged_idx_list) # Google出荷シートの反映済み（F）列を更新
    ######################### 更新ここまで #########################
    
    #print("\n更新後出荷シート: \n", ship_df) # DEBUG用

def update_error(prd_df, prd_sheet, error_n):
    write_error(prd_df, error_n) # エラーの数を更新
    ######################## シート更新 ######################
    write_error_gsheet(prd_sheet, error_n) # Google製造シートのエラーの数を更新
    ######################## 更新ここまで #####################


def update_each_item_n(prd_df, prd_sheet):
    # 各製造種目の在庫を更新（合計も計算）
    latest_stock_dict, stock_count = calc_latest_stock(prd_df) # 製造シート内の各アイスの現在（最新）の在庫を取得

    prd_df, updated_stock_ids = write_item_stock(prd_df, latest_stock_dict) # 製造シートの各アイスの冷凍庫内個数を更新（記録）
    ############################# シート更新 #############################
    write_stock_gsheet(prd_sheet, updated_stock_ids, latest_stock_dict) # Google製造シートの冷凍庫内個数（I）列を更新（記録）
    ############################ 更新ここまで ############################

    prd_df = write_prd_allstock(prd_df, stock_count) # 製造シートの合計を更新
    ################## シート更新 ##################
    write_allstock_gsheet(prd_sheet, stock_count) # Google製造シートの合計値（J2）を更新
    ################## 更新ここまで ##################


################################## POST ##################################