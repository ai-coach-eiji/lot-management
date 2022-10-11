from ..authentication import gsheet as gs
from ..manipulation.extract import column_as_list
from ..constant.item import item_dict
from ..constant.shipping import ship_dict

def get_item_info(params):
    # 出荷フォーム記入に必要な情報を取得
    params['item_dict'] = item_dict # 製造種目とそのID辞書
    params['ship_dict'] = ship_dict # 出荷先とそのID辞書

    prd_df, prd_sheet = gs.get_sheet_values("製造シート")
    qr_column_list = column_as_list(prd_df, "QR_No")
    qr_list = [qr for qr in qr_column_list if qr is not None]
    params['qr_list'] = qr_list # 製造シートのQR_No列
    return params