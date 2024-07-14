import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

import csv

# CSVファイルのパス
csv_file_path = 'C:\\Users\\kh111\\Desktop\\PythoTest\\銘柄.csv'

# CSVファイルから1列目（A列）のデータを読み込んでリストに格納
stock_symbols_jp = []

with open(csv_file_path, newline='') as csvfile:
    
    reader = csv.reader(csvfile)
    for row in reader:
        stock_symbols_jp.append(row[0])

# 一週間前の日付を計算
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

# データを格納するための空のデータフレームを作成
result_df = pd.DataFrame()

# 各銘柄の終値を取得
for symbol_jp in stock_symbols_jp:
    data = yf.download(symbol_jp, start=start_date, end=end_date)
    
    # 終値の列のみを抽出
    close_prices = data['Close']
    
    # 終値をデータフレームに追加
    result_df[symbol_jp] = close_prices

# 転置したデータフレームを新しい変数に格納
transposed_result_df = result_df.transpose()

# ファイルのパスを組み立ててCSVファイルに出力
file_path = file_path = 'C:\\Users\\kh111\\Desktop\\PythoTest\\株価.csv'
transposed_result_df.to_csv(file_path, index=True)

# 出力したファイルのパスを表示
print(f"CSVファイルが以下のパスに出力されました: {file_path}")

# 転置したデータフレームを表示（ここでは簡単な例として先頭5行を表示）
print(transposed_result_df.head())

