import time

from .get import get_all_qrs, get_row_values
from ..utils2.time import scanned_time

from ..manipulation.extract import get_idx, get_last_idx
from ..manipulation.write import write_prddone_gsheet, write_shipdone_gsheet, shift_prd_gsheet, shift_ship_gsheet
from ..constant.crop import prd_crop_list, ship_crop_list

def crop_info(prd_df, ship_df, done_df, done_sheet, prd_zero_list, params): # download view メイン処理
    # 製造&出荷シートの在庫0の情報を製造出荷完了シートに切り取る
    info_for_done = shift_prd_df(prd_df, prd_zero_list) # 在庫0の行があれば上につめる（切り取る）

    if info_for_done is not None:
        #print('\n製造出荷完了シートを作成します') # DEBUG用
        prd_gsheet_dict, ship_gsheet_list, qr_idx_dict = write_ps_done(ship_df, done_df, info_for_done) # 製造&出荷シートの情報を製造出荷完了シートに記録
        if ship_gsheet_list != []:
            #print('Googleの製造出荷完了シートを更新します') # DEBUG用
            ship_df = shift_ship_df(ship_df, qr_idx_dict) # 0. ship_dfを上につめる
            
            ######################### シート更新 #########################
            write_prddone_gsheet(prd_gsheet_dict, done_sheet) # 1. Googleの製造出荷完了シートにprd_dfから取得した値（辞書）を反映
            write_shipdone_gsheet(ship_gsheet_list, done_sheet) # 1. Googleの製造出荷完了シートにship_dfから取得した値（リスト内の辞書）を反映
            ######################## 更新ここまで #########################

            ######################### シート更新 #########################
            shift_ship_gsheet(ship_df, qr_idx_dict) # 2. Googleの出荷シートを上につめる（在庫が0になったもの）
            ######################### 更新ここまで #########################

            ######################### シート更新 #########################
            shift_prd_gsheet(prd_df, prd_zero_list) # 3. Googleの製造シートを上につめる（在庫が0になったもの）
            ######################### 更新ここまで #########################
            
            params['result'] = 'Google製造&出荷&製造出荷完了シートを更新しました'
            #print('Google製造&出荷&製造出荷完了シートを更新しました') # DEBUG用
        else:
            #params['Googleの製造出荷完了シートにすでに記載されている情報です']
            print('Googleの製造出荷完了シートにすでに記載されている情報です') # DEBUG用
    else:
        params['result'] = '製造出荷完了シートは最新状態です'
        #print('製造出荷完了シートに記載できる情報がありません') # DEBUG用
    return params

def write_ps_done(ship_df, done_df, info_for_done):
    # 製造&出荷シートの情報を製造出荷完了シートに記録
    done_df, qr_list, prd_gsheet_dict = write_prd2done(done_df, "タイムスタンプ", info_for_done) # 製造シートから切り取った情報を記載（基準となる列のidx: タイムスタンプ）
    #print('Googleの製造出荷完了シートに記載する製造シートから切り取った情報: ', prd_gsheet_dict) # DEBUG用
    #print("製造出荷完了シートに製造シートの情報を反映した後: \n", done_df) # DEBUG用

    #done_idx_series = done_df["row_idx"] # 製造シートの情報を反映した後に取得（行数が異なるため）
    qr_idx_dict = get_all_qrs(ship_df, qr_list) # 出荷シートから全てのQR_Noのidxリストを辞書で取得
    qr_values_dict = get_row_values(qr_idx_dict, ship_df) # 該当するQR_Noの情報（製造出荷完了シートに書きたい内容）を取得

    done_df, ship_gsheet_list = write_ship2done(done_df, qr_values_dict) # 出荷シートから切り取った情報を記載（基準となる列のidx: row_idx）      
    print("\n製造出荷完了シートに出荷シートの情報を反映した後: \n", done_df) # DEBUG用
    print("\nGoogleシートに記載する出荷シートの情報: \n", ship_gsheet_list) # DEBUG用
    return prd_gsheet_dict, ship_gsheet_list, qr_idx_dict

def shift_prd_df(prd_df, prd_zero_list):
    # 製造シートの在庫が0の行をすべて上につめる
    info_for_prdship = None
    if prd_zero_list != []:
        info_for_prdship = []
        for e in range(len(prd_zero_list)): # 製造シートの在庫が0だった行の個数分だけループ
            t_idx = get_idx(prd_df, "在庫", '0')
            #print('t_idx: ', t_idx) # DEBUG用
            prd_df, prd_info_list = shift_row(prd_df, prd_crop_list, t_idx) # t_idx番号に応じて1行上につめる
            info_for_prdship.append(prd_info_list)
        print('[shift_prd_df func] 製造出荷完了シートに貼り付ける内容: \n', info_for_prdship) # DEBUG用
        print('\n切り取り後のprd_df: \n', prd_df) # DEBUG用
    else:
        print('[shift_prd_df func] 在庫が0の製造種目はありません') # DEBUG用
    return info_for_prdship

def shift_ship_df(ship_df, qr_idx_dict):
    # 出荷シートの在庫が0の行をすべて上につめる
    print("出荷シートつめる前: \n", ship_df) # DEBUG用
    for qr, ship_zero_list in qr_idx_dict.items(): # k: QR_No, v: ship_zero_list（出荷シートの在庫が0のすべてのidx）
        if ship_zero_list != []:
            for _ in range(len(ship_zero_list)): # 出荷シートの在庫が0だった各QR_Noの個数（行数）分だけループ
                t_idx = get_idx(ship_df, "QR_No", qr) # つめる度にidxがズレるため、毎回在庫が0のQR_Noのidxを特定する
                ship_df, ship_info_list = shift_row(ship_df, ship_crop_list, t_idx) # t_idx番号に応じて1行上につめる
    print("出荷シートつめた後: \n", ship_df) # DEBUG用
    return ship_df

def shift_row(prd_df, crop_list, t_idx): # crop_list: utils.py参照
    # dfの特定の範囲を上につめる
    prd_df, prd_info_list = extract_row(prd_df, crop_list, t_idx) # 在庫が0のidxに合った1行を切り取る
    print(f"[shift_row func] シート{t_idx}行目から切り取った情報: ", prd_info_list) # DEBUG用

    # 在庫0のidx(t_idx)の行を上(periods=-1)につめる（末尾は0埋め）
    prd_df.loc[t_idx:, crop_list] = prd_df.loc[t_idx:, crop_list].shift(periods=-1, fill_value=None) # ToDo: NaNで埋められる（Noneにしたい）
    return prd_df, prd_info_list

def extract_row(df, crop_list, r): # crop_list: constant.cropで定義
    # 製造シートから切り取る1行の情報を抽出（この情報を後から製造出荷完了シートに貼り付ける）
    temp_list = []
    for c_name in crop_list:
        temp_list.append(df.at[r, c_name])
    return df, temp_list

def write_prd2done(done_df, column_name, info_for_done):
    # 製造シートの在庫が0になったすべての製造種目情報を製造出荷完了シートに記載する
    qr_list = []
    gsheet_dict = {} # Googleシート記載用の辞書
    for info_list in info_for_done:
        done_idx = get_last_idx(done_df, column_name)
        done_df, temp_l = write_row_prd2done(done_df, done_idx, info_list) # 製造シートから切り取った情報を記載
        gsheet_dict[done_idx] = temp_l[:6] # k: 製造出荷完了シートの空欄になっているidx, v: 製造シートの在庫が0になった1つのQR_Noの情報（リスト）
        qr_list.append(temp_l[1]) # 在庫が0のQR_No
    return done_df, qr_list, gsheet_dict

def write_row_prd2done(done_df, idx, info_list):
    # 製造シートから切り取った1行を製造出荷完了シートに記載する
    temp_l = done_df.loc[idx] # 最終行を一時的に取得

    for e, value in enumerate(info_list):
        if e == 0:
            temp_l[e] = scanned_time() # ボタンを押した日付を記載するため
        else:
            temp_l[e] = value
    done_df.loc[idx] = temp_l
    print('[write_row_prd2done func] 製造シートから記載した内容: ', done_df.loc[idx].values.tolist()) # DEBUG用
    return done_df, temp_l.values.tolist() # df と 記載した1行（リスト）

def write_ship2done(done_df, qr_values_dict):
    # 出荷シートのすべての情報を製造出荷完了シートに記載する
    ship2done_forGoogle_list = []
    for qr, idx_dict in qr_values_dict.items(): # k: QR_No, v: idx辞書
        print('idx_dict keys(): ', idx_dict.keys()) # DEBUG用

        t_dict = {} # gooleシート用の辞書（k: 記載するidx, v: 記載する値のリスト）
        for idx, v in idx_dict.items(): # k: idx, v: 各行の情報
            idx = str(idx+1) # +1はgoogleシート基準で見た時のidxにするため
            for _ in range(v[2]): # 出荷個数の数だけループを回す（22/10/09）
                info_list = [qr, v[0], v[1], idx] # [QR_No, 出荷日, 出荷先, 出荷シートのidx]
                
                df_series = done_df['row_idx'] # 各idxに対して行が増えるため、毎回上書きしないといけない
                #print("len: ", len(done_df), len(df_series)) # DEBUG用
                done_idx = get_last_idx(done_df, 'row_idx') # 製造出荷完了シートrow_idx列の最終行idxを取得
                print('int(idx): ', int(idx))
                target_row = done_df.loc[int(idx)].values.tolist()[7:] # 製造出荷完了シートの右側（H列〜K列）の行番号idxを一時的に取得
                if (qr in target_row) and (idx in target_row): # QR_Noとrow_idxが既にある場合はスキップ
                    print(f'出荷シートの{idx}行目のQR_No: {qr}は既に書き込まれているため、スキップします') # DEBUG用
                else:
                    done_df, temp_l = write_row_ship2done(done_df, done_idx, info_list) # 出荷シートから切り取った情報を記載
                    t_dict[done_idx] = info_list # k: gシートに記載するidx, v: gシートに記載する値のリスト

        if t_dict != {}:       
            ship2done_forGoogle_list.append(t_dict)
        else:
            print(f'QR_No: {qr}の情報はすでに書き込まれています') # DEBUG用
    return done_df, ship2done_forGoogle_list

def write_row_ship2done(done_df, idx, info_list):
    # 出荷シートから切り取った1行を製造出荷完了シートに記載する
    temp_l = done_df.loc[idx] # 最終行を一時的に取得

    for e in range(len(temp_l)):
        if e < 7:
            pass # 出荷シートの情報を書くのはdfの7列目から
        else:
            temp_l[e] = info_list[e-7] # info_listには順に次の値を格納: [QR_No, 出荷日, 出荷先, 出荷シートのidx]
    done_df.loc[idx] = temp_l
    print('[write_row_ship2done func] 出荷シートから記載した内容: ', done_df.loc[idx].values.tolist()) # DEBUG用
    return done_df, temp_l
