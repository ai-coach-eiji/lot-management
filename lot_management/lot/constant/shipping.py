# スキャンした際に、どの列に記録するか指定（df出荷シート）
write_ship_columns_list = ["タイムスタンプ", "QR_No", "出荷日", "出荷個数", "反映済み"]

# スキャンした際に、どの列に記録するか指定（Google出荷シート）
write_gshipsheet_columns_list = ["A", "B", "C", "E", "F"] # タイムスタンプ, QR_No, 出荷日, 出荷個数, 反映済みに対応

# ship_list: 出荷先を格納したリスト
ship_list = [
    'アイスクリンカフェアーク',
    'アイスクリンカフェMi-ma',
    '座覇笑店',
    'うるま屋',
    'ムーンアイス',
    'まーさんドッグ',
    '沖縄ベルク',
    'TOAmart',
    'キッチン名蔵', 
    'ペゴパ', 
    '今帰仁ダイニングE-DUME', 
    'その他'
]

# ship_id_list: 出荷先IDを格納したリスト
ship_id_list = [
    'AA',
    'AM',
    'ZS',
    'UY',
    'MA',
    'MD',
    'OB',
    'TM',
    'KN',
    'PP',
    'ED',
    'ST'
]

# 出荷先と出荷先IDの辞書
ship_dict = {id: name for id, name in zip(ship_id_list, ship_list)}
    