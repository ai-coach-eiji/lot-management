item_list = [
    'バニラ', 
    'チョコ', 
    'イチゴ', 
    'シークワーサー', 
    'マンゴー', 
    'ベニイモ', 
    'パイン', 
    'サトウキビ', 
    'タンカン', 
    'アセロラ', 
    'パッションフルーツ', 
    'ラムレーズン', 
    'レモングラス', 
    'グァバ', 
    'サクラ', 
    'シオ',
    'その他'
]

item_dict = {'{:0=2}'.format(i+1): item_list[i] for i in range(len(item_list))} # 2桁で0パディング