import pandas as pd

# CSVファイルのパス
csv_file_path = 'C:\\Users\\kh111\\Desktop\\PythoTest\\株価.csv'

# CSVファイルを読み込む
data = pd.read_csv(csv_file_path, index_col=0, parse_dates=True)

# A列の銘柄情報を取得
symbols = data.index

# 各銘柄ごとに5日移動平均を計算し、上昇トレンドを判定
for symbol in symbols:
    close_prices = data.loc[symbol]
    # 5日移動平均を計算
    ma_5days = close_prices.rolling(window=5).mean()
    # 最新の終値と移動平均を取得
    latest_close = close_prices.iloc[-1]
    latest_ma_5days = ma_5days.iloc[-1]
    # 上昇トレンドの判定
    if latest_close > latest_ma_5days:
        print(f"{symbol}: 上昇トレンド")
    else:
        print(f"{symbol}: 上昇トレンドではない")