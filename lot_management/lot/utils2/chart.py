import pandas as pd

import plotly.express as px
from plotly.offline import plot

from .time import scanned_time

def create_bar_chart(stock_items):
    # /lot/stock/ で、在庫（辞書型）を棒グラフで表示
    update_date = scanned_time() # 更新ボタンを押した日付を取得

    # 在庫文字列を数値に変換
    stock_items = {k: int(v) for k, v in stock_items.items()}
    chart_df = pd.DataFrame.from_dict(stock_items, orient='index').rename(columns={0:'冷凍庫内個数'})

    values_chart = chart_df['冷凍庫内個数'].values.tolist()
    #print("values_chart: ", values_chart) #DEBUG用

    fig = px.bar(chart_df, text=values_chart, title=f'{update_date} の冷凍庫内個数', color=values_chart, orientation="h")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, showlegend=False)
    fig.update_layout(title_x=0.5)
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(title_text="在庫")
    fig.update_yaxes(title_text="")

    plot_div = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return plot_div