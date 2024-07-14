import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

#1週間前からの株価データを取得（縦横入れ替え版）です
# 銘柄リスト（例：一部の企業の銘柄コード）
stock_symbols_jp = ["9984.T", "7203.T", "6758.T"]  # 任意の銘柄を指定

# 一週間前の日付を計算
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

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

