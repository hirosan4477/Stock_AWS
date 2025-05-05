import pandas as pd
from sqlalchemy import create_engine, text
import getpass

# CSVファイルパス（必要に応じて変更）
csv_file = r'C:\Users\kh111\Desktop\PythoTest\CSV\上場企業一覧.csv'
table_name = 'list'

# RDS接続情報
host = 'stock-db.cxuaca6uq8mz.ap-northeast-1.rds.amazonaws.com'
port = 3306
database = 'stockdb'  # ← Workbenchで作成したDB名
user = 'admin'

# パスワードを安全に取得（入力時に非表示）
password = getpass.getpass('stock0504!!')

# DBエンジン作成
engine = create_engine(
    f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
)

# CSV読み込み
df = pd.read_csv(csv_file)

# テーブルがあれば削除（エラー修正済み）
with engine.connect() as conn:
    conn.execute(text(f'DROP TABLE IF EXISTS `{table_name}`'))

# CSV → RDSへインポート
df.to_sql(table_name, engine, if_exists='replace', index=False)

print('✅ RDSにCSVデータをインポートしました。')
