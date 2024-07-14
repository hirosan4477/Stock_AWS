import pandas as pd

# CSVファイルのパス
csv_file_path = 'C:\\Users\\kh111\\Desktop\\PythoTest\\株価.csv'

# CSVファイルを読み込む（エンコーディングを指定）
data = pd.read_csv(csv_file_path, index_col=0, parse_dates=True, encoding='shift-jis')

# A列の銘柄情報を取得
symbols = data.index

# 新しい列を追加して、各銘柄の5日移動平均と上昇トレンドの判定結果を計算
for symbol in symbols:
    close_prices = data.loc[symbol]
    # 欠損値を前日の値で補完してから移動平均を計算
    close_prices.fillna(method='ffill', inplace=True)
    # 5日移動平均を計算
    ma_5days = close_prices.rolling(window=5).mean()
    # 最新の終値と移動平均を取得
    latest_close = close_prices.iloc[-1]
    latest_ma_5days = ma_5days.iloc[-1]
    # 上昇トレンドの判定
    if latest_close > latest_ma_5days:
        trend = "上昇トレンド"
    else:
        trend = "上昇トレンドではない"
    # 判定結果を新しい列に追記
    data.loc[symbol, "トレンド判定"] = trend

# CSVファイルに判定結果を上書き保存（エンコーディングをshift-jisに指定）
data.to_csv(csv_file_path, encoding='shift-jis')

print("判定結果を含むCSVファイルが上書き保存されました。")
