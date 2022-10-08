# product view の処理を担当

from ..constant.item import item_dict
from ..authentication import gsheet as gs

from ..manipulation.extract import create_prd
from ..manipulation.write import write_prd_gsheet


def create_product(params, prd_writing_date, post_dict):
    prd_df, prd_sheet = gs.get_sheet_values("製造シート") # シート名からその値を取得（pd用とgsheet更新用）
    updated_id, updated_row = create_prd(prd_df, prd_writing_date, post_dict) # 製造シートに製造情報を記入
    ############################## シート更新 ##############################
    write_prd_gsheet(prd_sheet, prd_writing_date, updated_id, updated_row) # Google製造シートに製造情報を記入
    ############################## 更新ここまで ##############################
    
    params['written'] = updated_id
    params['item_dict'] = item_dict

    return params