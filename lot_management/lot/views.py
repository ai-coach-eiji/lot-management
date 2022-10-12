from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.http import HttpResponseBadRequest

from django.conf import settings
from django.contrib import messages

from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import os
import json
import re

# 自作パッケージ
from .authentication import gsheet as gs
from .manipulation.extract import edit_shipping_byhand, get_idx_list
from .manipulation.write import write_shipping_byhand
from .utils2.time import scanned_time

from .constant.shipping import ship_dict
from .constant.item import item_dict

from .stream.process import Stream, gen
from .stock.process import get_stock, update_error, update_each_item_n, check_registered
from .product.process import create_product
from .download.process import crop_info
from .print.process import get_all_items, show_selected_items
from .scan.process import show_scan_result, write_ship_dest
from .shipping.process import get_item_info

@method_decorator(login_required, name='dispatch')
class MyPageView(TemplateView):
    template_name = 'lot/mypage.html'

@method_decorator(login_required, name='dispatch')
class PrintView(View): 
    template_name = 'lot/print.html'
    
    def get(self, request):
        params = {}
        params = get_all_items(params) # 印刷可能な製造種目を取得

        return render(request, self.template_name, params)
    
    def post(self, request, *args, **kwargs):
        post = request.POST
        params = {}

        if 'print' in post:
            post_dict = json.loads(request.POST["print"])
            #print("post:", post_dict) # DEBUG用

            params = show_selected_items(post_dict, params) # 選択した商品の情報を表示
            return render(request, self.template_name, params)
        else:
            return HttpResponseBadRequest()


@method_decorator(login_required, name='dispatch')
class DownloadView(View):
    template_name = 'lot/download.html'
    # {{ df_html|safe }} テンプレートに貼ると、スマホで崩れる
    
    def get(self, request):
        params = {}

        done_df, done_sheet = gs.get_sheet_values("製造出荷完了シート") # シート名からその値を取得（pd用とgsheet更新用）
        prd_df, prd_sheet = gs.get_sheet_values("製造シート")

        df_html = done_df.to_html() # 製造出荷完了シートをHTMLに変換
        params['df_html'] = df_html

        return render(request, self.template_name, params)
    
    def post(self, request, *args, **kwargs):
        post = request.POST
        params = {}
        save_date = scanned_time() # ボタンを押した日付をファイル名にするため

        if 'prd_download' in post:
            prd_df, prd_sheet = gs.get_sheet_values("製造シート")
            response = download_df(prd_df, save_date, 'production')
            return response

        if 'ship_download' in post:
            ship_df, ship_sheet = gs.get_sheet_values("出荷シート")
            response = download_df(ship_df, save_date, 'shipping')
            return response
        
        if 'create_done_sheet' in post:
            done_df, done_sheet = gs.get_sheet_values("製造出荷完了シート")
            prd_df, _ = gs.get_sheet_values("製造シート")
            ship_df, _ = gs.get_sheet_values("出荷シート")

            prd_zero_list = get_idx_list(prd_df, "在庫", '0') # 製造シートで、在庫が0になった製造種目のidxを取得
            #print('在庫が0のidxリスト: ', prd_zero_list) # DEBUG用

            params = crop_info(prd_df, ship_df, done_df, done_sheet, prd_zero_list, params) # 製造&出荷シートの在庫0の情報を切り取り、製造出荷完了シートに貼り付ける
            return render(request, self.template_name, params)
        else:
            return HttpResponseBadRequest()

def download_df(df, date, filename):
    # 1つのdfをcsvファイルとしてダウンロードする（zipでダウンロードできるようになるまで仮に使用する）
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    response['Content-Disposition'] = f'attachment; filename="{filename}_done_{date}.csv"'
    
    df.to_csv(path_or_buf=response, encoding='shift_jis', index=False)
    return response


@method_decorator(login_required, name='dispatch')
class ProductView(View):
    # 製造シートに製造情報を記入
    template_name = 'lot/product.html'
    
    def get(self, request):
        params = {}
        params['item_dict'] = item_dict
        return render(request, self.template_name, params)
    
    def post(self, request, *args, **kwargs):
        prd_writing_date = scanned_time() # 製造情報を入力している時の日付を取得
        params = {}

        post_dict = json.loads(request.POST["register"]) # テンプレートから入力された製造情報を取得
        #print("post:", post_dict) # DEBUG用

        params = create_product(params, prd_writing_date, post_dict) # 製造種目を記録
        return render(request, self.template_name, params)


@method_decorator(login_required, name='dispatch')
class StockView(View):
    # 在庫確認ページ
    template_name = 'lot/stock.html'
    
    def get(self, request):
        params = {}
        params, _ = get_stock(params) # 在庫数を辞書で取得（テンプレートに表示するため）

        return render(request, self.template_name, params)
    
    def post(self, request, *args, **kwargs):
        post = request.POST
        params = {}

        if 'refresh' in post: # 更新ボタンを押した時の処理
            prd_df, prd_sheet = gs.get_sheet_values("製造シート") # シート名からその値を取得（pd用とgsheet更新用）
            ship_df, ship_sheet = gs.get_sheet_values("出荷シート")

            params, prd_df, prd_sheet = check_registered(params, ship_df, ship_sheet, prd_df, prd_sheet) # 出荷シートの反映済み列をチェック
            update_each_item_n(prd_df, prd_sheet) # 各製造種目の在庫を更新（合計も計算）

            # 更新後の在庫を再度取得（反映された値を取得するため）
            params, error_n = get_stock(params)
            update_error(prd_df, prd_sheet, error_n) # エラー数を更新

            return render(request, self.template_name, params)
        else:
            return HttpResponseBadRequest()


@method_decorator(login_required, name='dispatch')
class EditView(View):
    template_name = 'lot/edit.html'

    def get(self, request):
        params = {}
        params = get_item_info(params) # 出荷フォーム画面記入に必要な情報を取得
        return render(request, self.template_name, params)
    
    def post(self, request, *args, **kwargs):
        edit_date = scanned_time() # 編集日付を取得
        params = {}

        post_dict = json.loads(request.POST["edit"])
        print("出荷フォームに記載した内容:\n", post_dict) # DEBUG用

        ship_df, ship_sheet = gs.get_sheet_values("出荷シート") # シート名からその値を取得（pd用とgsheet更新用）
        updated_id = edit_shipping_byhand(ship_df, edit_date, post_dict) # 出荷シートに商品情報を手書きで編集
        write_shipping_byhand(ship_sheet, edit_date, post_dict, updated_id) # Google出荷シートに編集内容を記録
        messages.success(request, '出荷シートに記録しました')

        return HttpResponseRedirect(reverse('lot:edit')) # ページ再読み込みの二重POST対策

        # params['written'] = updated_id # 編集内容を記載した行番号
        # params['item_dict'] = item_dict
        # params['ship_dict'] = ship_dict
        #return render(request, self.template_name, params)


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    template_name = 'lot/index.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request, *args, **kwargs):
        post = request.POST
        scan_date = scanned_time() # スキャンした日付を取得

        shipping = None
        params = {}

        if 'shipping' in post: # 出荷先の「確定」ボタンを押した場合
            comfirmed_ship_dest = str(request.POST.get('shipping')) # QRコード記載の出荷先を取得
            request, params = write_ship_dest(request, comfirmed_ship_dest, scan_date, params) # 出荷先を記録
        elif 'scan' in post: # （商品）QRコードをかざした場合
            ImageData = request.POST.get('scan') # ブラウザから画像を取得
            params = show_scan_result(ImageData, scan_date, params) # スキャン結果を表示
        else:
            return HttpResponseBadRequest()

        return render(request, self.template_name, params)

# ローカルPCのwebcamをopencvで起動する場合のみ有効
# def stream_view():
#     # WEBカメラの画像をストリーム配信
#     return lambda _: StreamingHttpResponse(gen(Stream()), content_type='multipart/x-mixed-replace; boundary=frame')