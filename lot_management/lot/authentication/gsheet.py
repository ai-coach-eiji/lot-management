import os

from django.conf import settings

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#from .sheet_keys import SPREADSHEET_KEY, json_name
from ..manipulation.extract import extract_as_df

import environ
env = environ.Env()
env.read_env('.env')
SPREADSHEET_KEY = env('SPREADSHEET_KEY')
json_name = env('JSON_NAME')


def get_sheet_values(sheet_name):
    # gsheetへの認証とそのファイル名から値を取得する
    workbook = google_auth() # gsheetにアクセスするための認証
    selected_values, selected_sheet = select_sheet(workbook, sheet_name) # シート名（変数: json_name）でアクセス
    selected_df = extract_as_df(selected_values)
    return selected_df, selected_sheet

def get_g_values(sheet_name):
    # gsheetへの認証とそのファイル名から値を取得する
    workbook = google_auth() # gsheetにアクセスするための認証
    selected_values, _ = select_sheet(workbook, sheet_name) # シート名（変数: json_name）でアクセス
    return selected_values

def get_worksheet_and_id(sheet_name):
    workbook = google_auth()
    selected_values, selected_sheet = select_sheet(workbook, sheet_name)
    selected_df = extract_as_df(selected_values)

    sheetId = selected_sheet._properties['sheetId'] # 範囲指定のupdateに必要
    return workbook, selected_df, sheetId

def google_auth():
    #jsonファイルを使って認証情報を取得
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    json_file = os.path.join(settings.BASE_DIR, 'lot/static/lot', json_name) #'lot-management-354410-d380611e06eb.json')
    c = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)

    #認証情報を使ってスプレッドシートの操作権を取得
    gs = gspread.authorize(c)

    #共有したスプレッドシートのキーを使ってシートの情報を取得
    workbook = gs.open_by_key(SPREADSHEET_KEY)
    return workbook

def select_sheet(workbook, sheet_name):
    # シート名でアクセスし、すべての値を取得
    worksheet = workbook.worksheet(sheet_name)

    all_values = worksheet.get_all_values()
    return all_values, worksheet

