from pyzbar.pyzbar import decode

from ..authentication import gsheet as gs
from ..constant.shipping import ship_dict
from ..manipulation.extract import extract_prd_date, get_idx, column_as_list
from ..manipulation.write import write_scanned_item

from ..utils2.improc import base64_to_cv, cv_to_base64
from ..utils2.draw import draw_msg, reference_item
from ..utils2.common import value_in, check_item, not_empty_list

def scan_img(image, ship_date):
    # スキャンした画像のQRコードを正しく読み込めればGoogleシートに記録

    decoded_list = decode(image) # QRコードの読み取り（QR_No）
    not_empty = not_empty_list(decoded_list) # 読み取った内容が空でないことを確認

    if not_empty: # QRコードの内容が読み取れた場合
        d_contents = decode_QR_No(decoded_list)

        # 出荷シートの情報だけ先に読み込んでおくと、出荷先のスキャンでも高速にレスポンスできる
        ship_df, ship_sheet = gs.get_sheet_values("出荷シート") # シート名からその値を取得（pd用とgsheet更新用）
        
        ################### 出荷先のスキャンはここから ###################
        if d_contents in ship_dict:
            ship_dest = ship_dict[d_contents]
            #print("出荷先のQRコードを読み取りました: ", ship_dest) # DEBUG用
            return None, ship_dest
        #################### 出荷先のスキャンはここまで ####################
        
        ##################### 商品のスキャンはここから #####################
        # [スキャン時点のタイムスタンプ, QR_No, 出荷日, 出荷個数, 反映済み]
        scan_temp = [ship_date, d_contents, ship_date, str(1), str(0)] # 出荷シートに記載する値を一時的なリストに格納
        # 出荷個数は 1 で固定（スキャンするのは１個づつなので）, 反映済みは 0 で固定（まだ反映してないので）

        prd_df, prd_sheet = gs.get_sheet_values("製造シート")
        image, included = search_QR(prd_df, d_contents, image) # シート内のQR_Noを探索し、出力画像に結果を描画

        if included:
            # QR_No製造日がdf出荷シート内にあった場合はスキャンした商品情報がGoogle出荷シートに記録される
            write_scanned_item(included, ship_df, ship_sheet, scan_temp)
        ###################### 商品スキャンここまで #######################
    
    else:
        #print("QRコードが確認できませんでした") # DEBUG用
        image = draw_msg(image, "QRコードの検出に失敗しました", (0,50,255), (120, 100), size=30)
    
    img_base64 = cv_to_base64(image) # ブラウザで表示できる形式に変換（cv2をbase64に）
    return img_base64, False

def decode_QR_No(decoded_list):
    # QRコードが映った画像の内容を取得
    d_contents = decoded_list[0].data.decode('utf-8')
    print(f"QR_No: {d_contents}") # DEBUG用
    return d_contents

def search_QR(prd_df, d_contents, image, same=False):
    # スキャンしたQR_Noを調べ、シート内にあれば記録できるようにする（same: 値が同じ時にTrue）

    lot_number_list, lot_date_str_list = get_qr_date(prd_df) # 製造シートからQR_No列と製造日列を取得

    prd_date = extract_prd_date(d_contents) # QRコードから日付(スラッシュ表記)を取得
    included = value_in(lot_date_str_list, prd_date) # QR_Noの製造日がシート内にあるか調べる

    if included: # QR_No製造日がシート内にある場合
        same = check_QR(prd_df, d_contents, qr_column="QR_No") # QR_No列とスキャンしたd_contentsを照合
        image = reference_item(image, d_contents, lot_number_list) # スキャンした商品名を画像に描画
    else:
        print("読み取った製造日はシートに存在しません") # DEBUG用
        image = draw_msg(image, "シートに存在しない製造日です!", (0,50,255), (120, 100), size=30)
    return image, same

def get_qr_date(prd_df):
    # 製造シートからQR_No列と製造日列を取得
    lot_numbers_list = column_as_list(prd_df, "QR_No")
    lot_dates_list = column_as_list(prd_df, "製造日")

    lot_dates_str_list = [str(d) for d in lot_dates_list] # 製造日を文字列リストとして抽出する
    #print("製造日一覧: ", lot_date_str) # DEBUG用

    return lot_numbers_list, lot_dates_str_list

def check_QR(prd_df, d_contents, qr_column="QR_No"):
    # QR_Noを照合（一致: True）
    qr_idx = get_idx(prd_df, qr_column, d_contents) # 特定の列（QR_No）に含まれる値（d_contents）のidxを取得
    if qr_idx != []:
        check_value = prd_df.at[qr_idx, qr_column] # シートにあるQR_Noを取り出してみる
    else:
        check_value = False
    return check_item(check_value, d_contents) # QR_Noを照合