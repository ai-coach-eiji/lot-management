from django.contrib import messages

from ..authentication import gsheet as gs

from ..manipulation.write import write_only_shipdest, write_shipdest_gsheet
from ..utils2.improc import base64_to_cv, cv_to_base64
from .scan_2 import scan_img

def get_valid(df, column_name):
    # 欠損値以外のリストを取得
    valid_list = df[df[column_name].values != None].index.tolist()
    print('[get_valid func] 有効値の最終行idx: ', valid_list[-1]) # DEBUG用
    return valid_list

def write_ship_dest(request, comfirmed_ship_dest, scan_date, params):
    ship_df, ship_sheet = gs.get_sheet_values("出荷シート") # シート名からその値を取得（pd用とgsheet更新用）

    updated_dest_list, empty_list = write_only_shipdest(ship_df, comfirmed_ship_dest, scan_date) # 出荷シートに出荷先を記録
    
    if empty_list != []:
        valid_list = get_valid(ship_df, "出荷先") # 出荷先が記入されている行番号を取得

        # 出荷先が記入されていない行番号があればユーザーに知らせる
        for i in empty_list:
            if i < valid_list[-1]: # 出荷先の最終行より小さいidxのみエラーの対象にする（大きいものはNoneなのでカウントしない）
                messages.warning(request, f'出荷先が記入されていない商品があります: {i+1}行目') # +1: pdのidxをgsheetに合わせるため

    if updated_dest_list == []: # 出荷先が更新されない時の処理
        params['date_mismatch'] = ['日付の不一致もしくはすべて更新済み']
    elif updated_dest_list is not None:
        params['updated_ship'] = updated_dest_list
        ######################### シート更新 #########################
        write_shipdest_gsheet(ship_sheet, comfirmed_ship_dest, updated_dest_list)
        ######################### 更新ここまで #########################
    else:
        params['no_candidate'] = ['すべての商品に出荷先が記入されています']

    return request, params
    

def show_scan_result(ImageData, scan_date, params):
    image = base64_to_cv(ImageData) # 画像処理できる形に変換

    scanned_img, shipping = scan_img(image, scan_date) # 出荷シートに商品情報を書き込むだけの処理
    params["image"] = scanned_img

    if not shipping :
        print('商品のスキャンが行われました（出荷先ではない）') # DEBUG用
    else:
        params['shipping_place'] = shipping # 出荷先をtemplateへ
        #print("出荷先: ", params.get('shipping_place')) # DEBUG用
    return params