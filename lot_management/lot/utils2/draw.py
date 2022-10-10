from PIL import ImageDraw, ImageFont

from ..constant.font import font_path, font_size # constantパッケージで定義
from ..constant.colors import orange, red # colorsパッケージで定義

from ..manipulation.extract import item_id_name
from .improc import cv_to_pil, pil_to_cv

def draw_msg(image, message, color, pos, size=None):
    # cv2画像に変数 message の内容を描画
    f_size = size or font_size # size指定があればその値を使用
    #print("font size", f_size) # DEBUG用

    img = cv_to_pil(image)
    draw = ImageDraw.Draw(img) # 描画用オブジェクト
    font = ImageFont.truetype(font_path, f_size) # PILでフォントを定義

    # テキストを描画（位置、文章、フォント、文字色（BGR+α）を指定）
    draw.text(pos, message, font=font, fill=color)
    image = pil_to_cv(img)
    return image

def reference_item(image, d_contents, lot_values_list):
    # 画像にスキャンした商品名を記載
    color = orange # 通常はオレンジ色で描画

    if d_contents in lot_values_list:
        _, item_name = item_id_name(d_contents)

        message = '読み取った商品名: ' + item_name
    else:
        message = '製造シート内の番号と一致しませんでした'
        color = red # エラーの場合は赤で描画

    image = draw_msg(image, message, color, (120, 100))
    return image

def draw_red(prd_df, error_list):
    # 出荷シートを編集する際にエラー（赤色）を描画
    red_list = []
    for i in error_list:
        red_list.append(prd_df.at[i, '製造種目'])
    print("[draw_red func] 在庫がマイナスの製造種目リスト: ", red_list) # DEBUG用
    return red_list