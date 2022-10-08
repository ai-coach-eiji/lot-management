def value_in(base_list, target):
    # 対象の値（target）がリスト（base_list）内にあるか判定
    included = False

    if target in base_list:
        included = True
        print('一致する日付を確認しました') # DEBUG用
    else:
        print(f"対象の値: {target}は以下のリストに存在しません\n{base_list}") # DEBUG用
    return included

def check_item(check_value, target):
    # 特定の値（target）が check_value と一致するか判定
    same = False
    msg = f'target: {target}とシートの値: {check_value}が'

    if check_value == target:
        same = True
        msg += '一致しました'
    else:
        msg += '一致しませんでした'

    print(msg) # DEBUG用
    return same

def not_empty_list(target_list, not_empty=False):
    # リストの中身が空かどうか調べる
    if target_list != []:
        not_empty = True
    else:
        print('リストは空です')
    return not_empty