from ..authentication import gsheet as gs
from ..constant.print import print_ship_list, print_list
from ..manipulation.extract import column_as_list, item_id_name, get_idx, get_idx_list

def get_all_items(params):
    done_df, done_sheet = gs.get_sheet_values("製造出荷完了シート") # シート名からその値を取得（pd用とgsheet更新用）
    done_list = column_as_list(done_df, "QR__No") # 製造の方のQR__Noを選択
    prd_date_list = column_as_list(done_df, "製造日") # 製造日を選択

    print_dict = create_print_dict(done_list, prd_date_list) # 製造出荷完了シート（つまり在庫が0）にある商品を抽出する
    params['print_dict'] = print_dict
    return params

def create_print_dict(qr_list, prd_date_list):
    print_items = {}
    for qr, date in zip(qr_list, prd_date_list):
        if qr is not None:
            item_number, item_name = item_id_name(qr)
            print_items[qr] = [item_name, date]
        else:
            print(f"[create_print_dict func] {len(print_items)}つの商品を選択できます") # DEBUG用
            break
    return print_items


def show_selected_items(post_dict, params):
    done_df, done_sheet = gs.get_sheet_values("製造出荷完了シート") # シート名からその値を取得（pd用とgsheet更新用）

    qr_no = post_dict["選択された商品"] # 選択された「印刷しする情報（QR_No）」
    selected_idx = get_idx(done_df, "QR__No", qr_no)
    selected_series = done_df.iloc[selected_idx-1, 1:6]
    print("選択された1行: ", selected_series) # DEBUG用

    sumit_list, stock = create_submit_list(selected_series) # 選択された1行から印刷に必要な情報を抽出
    submit_dict = create_submit_dict(sumit_list)
    params['submit_dict'] = submit_dict
    print('submit_dict: ', submit_dict) # DEBUG用

    params['ship_header'] = print_ship_list # 記録表に記載する出荷タイトル

    done_ship_list = get_idx_list(done_df, "QR_No", qr_no) # 製造出荷完了シートの出荷情報から一致するQR_Noのidxを抽出
    submit_ship_dict = create_submit_ship_dict(done_df, done_ship_list, int(stock))
    params['submit_ship_dict'] = submit_ship_dict
    return params


def create_submit_ship_dict(done_df, done_ship_list, stock):
    submit_ship_dict = {}
    for i in done_ship_list:
        stock -= 1 # 在庫が1つづつ減ると仮定
        selected_series = done_df.iloc[i-1, 7:11]
        selected_list = selected_series.values.tolist()

        shipped_date = selected_list[1] # 出荷日
        shipped_dest = selected_list[2] # 出荷先
        shipsheet_row_idx = selected_list[3] # 出荷シートの行番号（識別のためだけに用いる）
        sumit_list = [shipped_date, shipped_dest, 1, 'パック', stock, '']
        submit_ship_dict[shipsheet_row_idx] = sumit_list # 出荷シートの行番号を識別用のキーとする
    return submit_ship_dict

def create_submit_list(selected_series):
    selected_list = selected_series.values.tolist()

    item_name = f'ラクトアイス {selected_list[2]}'
    prd_date = selected_list[1]
    item_number = selected_list[3]

    sumit_list = [item_name, prd_date, '製造日で管理', item_number, '無し']
    return sumit_list, item_number

def create_submit_dict(sumit_list):
    submit_items = {}
    for p, s in zip(print_list, sumit_list):
        submit_items[p] = s
    return submit_items