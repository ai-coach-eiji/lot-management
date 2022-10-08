from ..manipulation.extract import get_idx_list

def get_all_qrs(ship_df, qr_list):
    qr_chage_dict = {}
    print("出荷シートの在庫が0になったすべてのQR_No行番号: \n") # DEBUG用
    for qr in qr_list: # 在庫が0のQR_Noを全て調べる
        qr_zero_list = get_idx_list(ship_df, "QR_No", qr)
        qr_chage_dict[qr]= qr_zero_list
    print('記載するQR_Noのidxリストを保持する辞書（qr_chage_dict）: ', qr_chage_dict) # DEBUG用
    return qr_chage_dict # key: QR_No, value: 該当するidxのリスト

def get_row_values(qr_dict, ship_df):
    qr_value_dict = {}
    for k, v_list in qr_dict.items():
        temp_d = {} # 製造出荷完了シートのH〜K列に記載する内容（1行）
        for v in v_list:
            shipped_n = int(ship_df.at[v, '出荷個数'])
            temp_d[v] = [ship_df.at[v, "出荷日"], ship_df.at[v, "出荷先"], shipped_n] # key: idx, value: [出荷日, 出荷先, 出荷個数（手動の編集に対応するため）]
            # if shipped_n == 1:
            #     temp_d[v] = [ship_df.at[v, "出荷日"], ship_df.at[v, "出荷先"]] # key: idx, value: [出荷日, 出荷先]
            # elif shipped_n > 1: # 出荷個数が2以上の場合（編集画面にて出荷情報を記載したとき）見やすくするために row_idxはidx*1000を加算
            #     temp_d = {}
            #     for i in range(shipped_n):
            #         temp_d[v+i*1000] = [ship_df.at[v, "出荷日"], ship_df.at[v, "出荷先"]] # key: idx, value: [出荷日, 出荷先]

        qr_value_dict[k] = temp_d # key: QR_No, value: 該当するidxのvalues
    print("[get_row_values func] 記載したい値を保持した辞書（qr_value_dict）: ", qr_value_dict)
    return qr_value_dict